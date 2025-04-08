#!/usr/bin/env python3
# type: ignore

"""View a CSV file using a textual interface."""

from __future__ import annotations

import csv
import operator
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import click
from polykit.core import polykit_setup
from textual import on
from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal
from textual.reactive import reactive
from textual.widgets import Button, DataTable, Footer, Header, Input, RichLog, Static, Tree

polykit_setup()


class CSVViewer(App):
    """View a CSV file using a textual interface."""

    CSS_PATH = Path(Path.parent(__file__)) / "csv_viewer.css"

    # Style settings
    MIN_VALUE_WIDTH = 25  # Minimum width for the "Value" column

    with Path(CSS_PATH).open(encoding="utf-8") as css_file:
        CSS = css_file.read()

    data: reactive[defaultdict[str, defaultdict[str, int]]] = reactive(
        defaultdict(lambda: defaultdict(int))
    )
    total_rows: reactive[int] = reactive(0)
    selected_column: reactive[str] = reactive("")
    selected_row: reactive[int] | reactive[None] = reactive(None)
    global_filter: reactive[dict[str, set]] = reactive({})
    filtered_data: reactive[defaultdict[str, defaultdict[str, int]]] = reactive(
        defaultdict(lambda: defaultdict(int))
    )
    sort_column: reactive[str] = reactive("")
    sort_reverse: reactive[bool] = reactive(False)

    def __init__(self, filename: str, show_log: bool):
        super().__init__()
        self.filename: str = filename
        self.all_rows: list = []  # Store all original rows
        self.filtered_rows: list = []
        self.show_log: bool = show_log

    def compose(self) -> ComposeResult:
        """Compose the application layout."""
        yield Header()
        yield Tree("Columns", id="column_tree")
        yield Container(
            Static("Global Filter: None", id="global_filter_info"),
            Static("Select a column to view details", id="details_header"),
            Horizontal(
                Input(placeholder="Filter values...", id="filter_input"),
                Button("Apply Filter", id="apply_filter"),
                Button("Clear Filters", id="clear_filters"),
                id="filter_container",
            ),
            DataTable(id="details_table", show_cursor=True),
            id="main_container",
        )
        if self.show_log:
            yield Container(RichLog(id="log"), id="log_container")
        yield Footer()

    def on_mount(self) -> None:
        """Load the data and populate the tree."""
        self.print_log("Application mounted. Loading data...")
        self.load_data()
        self.populate_tree()
        self.query_one("#column_tree").root.expand()
        self.setup_data_table()
        self.query_one("#column_tree").focus()

    def load_data(self) -> None:
        """Load the data from a CSV file."""
        self.print_log(f"Loading data from {self.filename}")
        with Path(self.filename).open(encoding="utf-8") as file:
            reader = csv.DictReader(file)
            self.all_rows = list(reader)  # Store all original rows
            self.filtered_rows = self.all_rows.copy()  # Initialize filtered rows with all rows
            for row in self.all_rows:
                self.total_rows += 1
                for col, value in row.items():
                    self.data[str(col)][str(value)] += 1
        self.print_log(f"Loaded {self.total_rows} rows of data")
        self.print_log(f"Columns found: {', '.join(self.data.keys())}")

    def setup_data_table(self) -> None:
        """Set up the DataTable with sortable headers."""
        table = self.query_one(DataTable)
        table.add_column("Value", key="value", width=self.MIN_VALUE_WIDTH)
        table.add_column("Count", key="count")
        table.add_column("Percentage", key="percentage")
        table.cursor_type = "row"

    def populate_tree(self) -> None:
        """Populate the tree with the columns and their unique value counts."""
        tree = self.query_one("#column_tree", Tree)
        for column, values in self.data.items():
            unique_count = len(values)
            node_label = f"{column} ({unique_count})"
            tree.root.add_leaf(node_label)
        tree.root.expand()  # Expand the root node to show all columns
        self.print_log(f"Populated tree with {len(self.data)} columns")

    def update_tree_counts(self) -> None:
        """Update the counts in the tree nodes based on the filtered data."""
        counts = {}

        # Recalculate column counts based on filtered rows
        for col in self.data:
            unique_values = set()
            for row in self.filtered_rows:
                value = row.get(col, "")
                value = "(no value)" if value in {None, ""} else value
                unique_values.add(value)
            counts[col] = len(unique_values)

        # Update the tree node labels with new counts
        tree = self.query_one("#column_tree", Tree)
        for node in tree.root.children:
            col_name = str(node.label).split(" (")[0]
            count = counts.get(col_name, 0)
            node.set_label(f"{col_name} ({count})")

    def on_tree_node_selected(self, event: Tree.NodeSelected) -> None:
        """Update the details when a tree node is selected."""
        self.selected_column = str(event.node.label).split(" (")[0]  # Extract just the column name
        self.query_one("#filter_input").value = ""
        self.print_log(f"Selected column: {self.selected_column}")
        self.update_details()

    def on_data_table_header_selected(self, event: DataTable.HeaderSelected) -> None:
        """Handle sorting when a column header is clicked."""
        if self.sort_column == event.column_key:
            self.sort_reverse = not self.sort_reverse
        else:
            self.sort_column = event.column_key
            self.sort_reverse = False
        self.update_details()

    def on_data_table_row_selected(self, event: DataTable.RowSelected) -> None:
        """Handle row selection in the DataTable."""
        self.selected_row = event.row_key
        table = self.query_one(DataTable)
        row = table.get_row(event.row_key)
        selected_value = row[0] if row else ""
        self.query_one("#filter_input").value = str(selected_value)
        self.print_log(f"Selected row: {selected_value}")

    def apply_filter(self) -> None:
        """Apply the filter to the current column data and update global filter."""
        filter_text = self.query_one("#filter_input").value.strip()
        self.print_log(f"Applying filter - Text: '{filter_text}', Column: {self.selected_column}")

        if filter_text:
            if self.selected_column not in self.global_filter:
                self.global_filter[self.selected_column] = set()
            self.global_filter[self.selected_column].add(filter_text)
            self.print_log(f"Added to global filter: {self.selected_column}: {filter_text}")
        elif self.selected_column in self.global_filter:
            del self.global_filter[self.selected_column]
            self.print_log(f"Removed from global filter: {self.selected_column}")

        self.apply_global_filter()
        self.update_global_filter_info()
        self.update_details()
        self.print_log(f"Global filter after update: {self.global_filter}")
        self.selected_row = None  # Reset selected row after applying filter

    def on_clear_filters(self) -> None:
        """Handle clear filters button press."""
        self.global_filter.clear()
        self.filtered_rows = self.all_rows.copy()  # Reset to original data
        self.query_one("#filter_input").value = ""
        self.update_global_filter_info()
        self.update_tree_counts()  # Update counts after clearing filters
        self.update_details()
        self.print_log("Cleared all filters.")

    def apply_global_filter(self) -> None:
        """Apply global filter to the entire dataset."""
        if not self.global_filter:
            self.filtered_rows = self.all_rows.copy()  # Reset to original data
            self.print_log("No global filter, using all rows")
        else:
            self.print_log(f"Applying global filter: {self.global_filter}")
            self.filtered_rows = [
                row
                for row in self.all_rows
                if all(
                    any(
                        filter_value.lower() in str(row.get(col, "")).lower()
                        for filter_value in values
                    )
                    for col, values in self.global_filter.items()
                )
            ]
            self.print_log(f"Filtered rows count: {len(self.filtered_rows)}")
        self.update_tree_counts()  # Update counts after filtering

    @on(Button.Pressed, "#apply_filter")
    def on_apply_filter(self) -> None:
        """Handle apply filter button press."""
        self.apply_filter()

    @on(Input.Submitted, "#filter_input")
    def on_filter_submitted(self) -> None:
        """Handle filter input submission (Enter key)."""
        self.apply_filter()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses."""
        if event.button.id == "apply_filter":
            self.apply_filter()
        elif event.button.id == "clear_filters":
            self.on_clear_filters()

    def update_global_filter_info(self) -> None:
        """Update the global filter information display."""
        filter_info = "Global Filter: "
        if self.global_filter:
            filter_info += ", ".join(
                f"{col} ({len(values)} values)" for col, values in self.global_filter.items()
            )
        else:
            filter_info += "None"
        self.query_one("#global_filter_info").update(filter_info)

    def update_details(self) -> None:
        """Update the details table with the selected column data."""
        header = self.query_one("#details_header", Static)
        table = self.query_one("#details_table", DataTable)

        header.update(f"Details for: {self.selected_column}")

        table.clear(columns=True)

        # Count occurrences in filtered rows
        filtered_data = defaultdict(int)
        for row in self.filtered_rows:
            value = row.get(self.selected_column, "")
            # Replace empty or None values with "(no value)"
            value = "(no value)" if value in {None, ""} else value
            filtered_data[value] += 1

        sorted_data = list(filtered_data.items())
        total_filtered_count = sum(count for _, count in sorted_data)

        # Prepare data for sorting and calculate max widths
        table_data = []
        max_value_width = len("Value")
        max_count_width = len("Count")
        max_percentage_width = len("Percentage")

        for value, count in sorted_data:
            percentage = (count / total_filtered_count) * 100 if total_filtered_count > 0 else 0
            percentage_str = f"{percentage:.2f}%"
            table_data.append((str(value), count, percentage_str))

            max_value_width = max(max_value_width, len(str(value)))
            max_count_width = max(max_count_width, len(str(count)))
            max_percentage_width = max(max_percentage_width, len(percentage_str))

        # Set minimum width for value to avoid having a tiny column
        max_value_width = max(max_value_width, self.MIN_VALUE_WIDTH)

        # Set default sorting if not specified
        if not self.sort_column:
            self.sort_column = "count"
            self.sort_reverse = True

        # Log sorting information
        self.print_log(f"Sorting by: {self.sort_column}, Reverse: {self.sort_reverse}")

        # Sort the data based on the selected column and direction
        if self.sort_column == "value":
            table_data.sort(key=operator.itemgetter(0), reverse=self.sort_reverse)
        elif self.sort_column == "count":
            table_data.sort(key=operator.itemgetter(1), reverse=self.sort_reverse)
        elif self.sort_column == "percentage":
            table_data.sort(key=lambda x: float(x[2][:-1]), reverse=self.sort_reverse)

        # Add columns with calculated widths
        table.add_column("Value", key="value", width=max_value_width)
        table.add_column("Count", key="count", width=max_count_width)
        table.add_column("Percentage", key="percentage", width=max_percentage_width)

        self.print_log(f"Updating details for column: {self.selected_column}")
        self.print_log(f"Total filtered rows: {len(self.filtered_rows)}")

        # Add rows to the table
        for row in table_data:
            table.add_row(*row)

        if not table_data:
            table.add_row("No data available", "", "")

        if table.row_count > 0:
            # Focus the DataTable and set the cursor to the first cell
            table.focus()
            table.cursor_coordinate = (0, 0)
            # Select the first cell
            table.selection = {(0, 0)}
            # Get the column index for the "value" column
            value_column_index = table.get_column_index("value")
            # Get the value from the first row's "Value" column
            first_row_value = table.get_cell_at((0, value_column_index))
            # Populate the "Apply Filter" input with this value
            self.query_one("#filter_input", Input).value = first_row_value

        self.print_log(f"Updated table with {len(table_data)} rows for {self.selected_column}")
        table.refresh(layout=True)

    def print_log(self, message: str) -> None:
        """Log a message to the RichLog widget and debug file."""
        if self.show_log:
            log_widget = self.query_one(RichLog)
            timestamp = datetime.now(tz=ZoneInfo("America/New_York")).strftime("%I:%M:%S %p")
            log_message = f"[{timestamp}] {message}"
            log_widget.write(log_message)
        self.log_to_file(message)

    def log_to_file(self, message: str) -> None:
        """Write a debug message to a file."""
        log_dir = Path.home() / ".local" / "share" / "csv_viewer" / "logs"
        log_dir.mkdir(parents=True, exist_ok=True)
        log_file = log_dir / "app.log"

        timestamp = datetime.now(tz=ZoneInfo("America/New_York")).strftime("%Y-%m-%d %H:%M:%S")
        with Path(log_file).open("a", encoding="utf-8") as f:
            f.write(f"{timestamp}: {message}\n")


@click.command()
@click.argument("filename", type=click.Path(exists=True))
@click.option("--show-log", is_flag=True, help="Show the log viewer in the application")
def main(filename: str, show_log: bool) -> None:
    """Run the application."""
    app = CSVViewer(filename, show_log)
    app.run()


if __name__ == "__main__":
    main()
