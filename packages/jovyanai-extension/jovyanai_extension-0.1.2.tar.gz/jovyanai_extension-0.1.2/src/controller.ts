// // Controller for the cellOps extension, responsible for handling the cellOps extension's state and interactions between the components
import { Cell } from '@jupyterlab/cells';
import { INotebookTracker } from '@jupyterlab/notebook';
import { CommandRegistry } from '@lumino/commands';

export class NotebookController {
  private _notebookTracker: INotebookTracker;
  private _commands: CommandRegistry;

  constructor(notebookTracker: INotebookTracker, commands: CommandRegistry) {
    this._notebookTracker = notebookTracker;
    this._commands = commands;
  }

  public get activeCell() {
    return this._notebookTracker.currentWidget?.content.activeCell;
  }

  public addElementAfterCellInput(cell: Cell, element: HTMLElement) {
    const cellNode = cell.node;
    // Append the parentContainer to the input area of the cell
    const inputArea = cellNode.querySelector('.jp-Cell-inputWrapper');
    if (inputArea) {
      inputArea.insertAdjacentElement('afterend', element);
    } else {
      cellNode.appendChild(element);
    }
  }

  public addElementInCellChild(cell: Cell, element: HTMLElement) {
    const cellNode = cell.node;
    cellNode.appendChild(element);
  }

  public writeCodeInCell(cell: Cell, code: string) {
    cell.model.sharedModel.setSource(code);
  }

  public runCell(cell: Cell) {
    const notebook = this._notebookTracker.currentWidget;
    if (notebook) {
      notebook.content.activeCellIndex = notebook.content.widgets.indexOf(cell);
      this._commands.execute('notebook:run-cell');
    }
  }

  public insertCell(index: number, content?: string) {
    const notebook = this._notebookTracker.currentWidget;
    if (notebook) {
      notebook.model?.sharedModel.insertCell(index, {
        cell_type: 'code',
        source: content
      });
    }
  }

  public get currentCell() {
    return this._notebookTracker.currentWidget?.content.activeCell;
  }

  public get currentCellIndex(): number {
    return this._notebookTracker.currentWidget?.content.activeCellIndex || 0;
  }

  public getPreviousCells(cell: Cell): Cell[] {
    const notebook = this._notebookTracker.currentWidget?.content;
    const index = notebook?.activeCellIndex;
    if (index !== undefined && notebook) {
      return notebook.widgets.slice(0, index);
    }
    return [];
  }

  public getNextCells(cell: Cell): Cell[] {
    const notebook = this._notebookTracker.currentWidget?.content;
    const index = this.currentCellIndex;
    if (index !== undefined && notebook) {
      return notebook.widgets.slice(index + 1);
    }
    return [];
  }

  public getLanguage() {
    const notebook = this._notebookTracker.currentWidget?.model;
    const language = notebook?.defaultKernelLanguage || 'python';
    return language;
  }

  public runCommand(command: string) {
    this._commands.execute(command);
  }
}
