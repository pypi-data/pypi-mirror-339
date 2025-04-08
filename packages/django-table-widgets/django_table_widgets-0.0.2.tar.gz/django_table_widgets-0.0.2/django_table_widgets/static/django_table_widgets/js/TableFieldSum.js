class TableFieldSumWidget {
  constructor(options) {
    this.options = {
      rowsCount: 0,
      columnsCount: 0,
      showRowSum: false,
      showColumnSum: false,
      showTableSum: false,
      listenedEvent: "input",
    };

    // Altering using user-provided options
    for (const property in options) {
      if (options.hasOwnProperty(property)) {
        this.options[property] = options[property];
      }
    }

    this.table = document.getElementById(this.options.tableId);

    this.table.querySelectorAll("input").forEach(input => {
      if (this.options.showRowSum) {
        input.addEventListener(this.options.listenedEvent, (event) => {
          const rowIndex = event.target.parentElement.dataset.rowIndex;
          this.updateRowSum(rowIndex);
        });
      }

      if (this.options.showColumnSum) {
        input.addEventListener(this.options.listenedEvent, (event) => {
          const columnIndex = event.target.parentElement.dataset.columnIndex;
          this.updateColumnSum(columnIndex);
          this.updateTableSum();
        });
      }

      if (this.options.showTableSum) {
        input.addEventListener(this.options.listenedEvent, (event) => {
          this.updateTableSum();
        });
      }
    });

    if (this.options.showRowSum) {
      for (let i = 0; i < this.options.rowsCount; i++) {
        this.updateRowSum(i);
      }
    }

    if (this.options.showColumnSum) {
      for (let i = 0; i < this.options.columnsCount; i++) {
        this.updateColumnSum(i);
      }
    }

    if (this.options.showTableSum) {
      this.updateTableSum();
    }
  }

  updateRowSum(rowIndex) {
    const rowCells = this.table.querySelectorAll(`td[data-row-index="${rowIndex}"] input`);
    const rowSum = Array.from(rowCells).reduce((sum, input) => {
      const value = parseInt(input.value) || 0;
      return sum + value;
    }, 0);

    const rowSumCell = this.table.querySelector(`td[data-row-sum="${rowIndex}"]`);
    rowSumCell.textContent = rowSum;
  }

  updateColumnSum(columnIndex) {
    const columnCells = this.table.querySelectorAll(`td[data-column-index="${columnIndex}"] input`);
    const columnSum = Array.from(columnCells).reduce((sum, input) => {
      const value = parseInt(input.value) || 0;
      return sum + value;
    }, 0);

    const columnSumCell = this.table.querySelector(`td[data-column-sum="${columnIndex}"]`);
    columnSumCell.textContent = columnSum;
  }

  updateTableSum() {
    const cells = this.table.querySelectorAll(`td input`);
    const tableSum = Array.from(cells).reduce((sum, input) => {
      const value = parseInt(input.value) || 0;
      return sum + value;
    }, 0);

    const tableSumCell = this.table.querySelector(`td[data-table-sum]`);
    tableSumCell.textContent = tableSum;
  }
}
