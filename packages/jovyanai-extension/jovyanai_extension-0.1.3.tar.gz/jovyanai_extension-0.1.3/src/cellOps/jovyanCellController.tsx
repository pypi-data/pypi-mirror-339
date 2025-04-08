import { Cell } from '@jupyterlab/cells';
import { CodeCellModel } from '@jupyterlab/cells';
import { createRoot } from 'react-dom/client';
import React from 'react';

import { NotebookController } from '../controller';

import ActivateCellButton from './components/ActivateCellButton';
import FixErrorButton from './components/FixErrorButton';
import InputComponent from './components/CellPromptInput';
import { DiffReview } from './components/DiffReview';

import { setupCodeGenerationStream } from '../handleCodeGeneration';

export class JovyanCellController {
  // Manage the UI to prompt AI on a cell
  private _cell: Cell;
  private _notebookController: NotebookController;

  constructor(cell: Cell, notebookController: NotebookController) {
    this._cell = cell;
    this._notebookController = notebookController;
  }

  public removeAllActivateButtons() {
    const button = document.querySelector('.jv-cell-ai-button-container');
    if (button) {
      button.remove();
    }
  }

  public removeCellActivateButton() {
    const button = this._cell.node.querySelector(
      '.jv-cell-ai-button-container'
    );
    if (button) {
      button.remove();
    }
  }

  public activate() {
    console.debug('Activating cell', this._cell.node);
    // remove all existing buttons
    this.removeAllActivateButtons();

    // add the button to the cell
    this.addCellActivateButton();
    this.addFixErrorButton();
  }

  public addCellActivateButton = () => {
    // remove all existing buttons
    this.removeAllActivateButtons();

    // if cell has code, show generate code button
    // if cell has no code, show change code button
    let text = 'Generate';
    if (this._cell.model.type === 'code') {
      const codeCellModel = this._cell.model as CodeCellModel;
      if (codeCellModel.sharedModel.source) {
        text = 'Modify';
      }
    }

    const buttonContainer = document.createElement('div');
    const root = createRoot(buttonContainer);

    const cellNode = this._cell.node;

    const handleClick = () => {
      this.addPromptInput();
      buttonContainer.remove();
    };
    const button = React.createElement(ActivateCellButton, {
      onClick: handleClick,
      text: text
    });
    root.render(button);
    cellNode.appendChild(buttonContainer);

    // add event listener to the cell to catch the keydown event
    if (!cellNode.hasAttribute('jv-activate-listener')) {
      cellNode.addEventListener('keydown', event => {
        if (event.key === 'k' && event.metaKey) {
          event.preventDefault();
          handleClick();
        }
      });
      // Mark the cell as having the listener attached
      cellNode.setAttribute('jv-activate-listener', 'true');
    }
  };

  public _checkIsErrorCell() {
    if (this._cell.model.type !== 'code') {
      return false;
    }
    const codeCellModel = this._cell.model as CodeCellModel;
    if (codeCellModel.sharedModel.outputs.length === 0) {
      return false;
    }
    for (const output of codeCellModel.sharedModel.outputs) {
      if (output.output_type === 'error') {
        return true;
      }
    }
    return false;
  }

  public addFixErrorButton() {
    if (this._cell.model.type !== 'code') {
      return;
    }
    console.debug('Adding fix error button', this._cell.node);

    // check if error button already exists
    const errorButton = this._cell.node.querySelector(
      '.jv-cell-fix-error-container'
    );
    if (errorButton) {
      return;
    }

    // add button to cell output node
    const cellNode = this._cell.node;
    const outputArea = cellNode.querySelector(
      '.jp-Cell-outputArea'
    ) as HTMLElement;
    if (!outputArea) {
      return;
    }

    if (!this._checkIsErrorCell()) {
      return;
    }

    const buttonContainer = document.createElement('div');
    const root = createRoot(buttonContainer);

    const handleClick = async () => {
      if (!this._checkIsErrorCell()) {
        return;
      }
      this._checkIsErrorCell();
      const codeStream = await this.createCodeStream('Fix this error');
      this.addDiffReview(codeStream);
      buttonContainer.remove();
    };
    const button = React.createElement(FixErrorButton, {
      onClick: handleClick,
      text: 'Fix Error'
    });
    root.render(button);
    outputArea.appendChild(buttonContainer);

    // Add event listener only if it doesn't exist already
    // Use a custom attribute to check if the listener is already attached
    if (!cellNode.hasAttribute('jv-fix-error-listener')) {
      cellNode.addEventListener('keydown', (event: KeyboardEvent) => {
        if (event.key === 'F' && event.shiftKey) {
          event.preventDefault();
          handleClick();
        }
      });
      // Mark the cell as having the listener attached
      cellNode.setAttribute('jv-fix-error-listener', 'true');
    }
  }

  public addPromptInput() {
    const cellNode = this._cell.node;
    if (cellNode.querySelector('.jv-cell-ai-input-container')) {
      console.debug('input container already exists');
      return;
    }

    const inputContainer = document.createElement('div');
    inputContainer.style.position = 'relative';
    inputContainer.style.marginTop = '10px';

    const inputComponent = React.createElement(InputComponent, {
      isEnabled: true,
      placeholderEnabled: 'Ask Jovyan',
      placeholderDisabled: 'Input disabled',
      onSubmit: async (input: string) => {
        const codeStream = await this.createCodeStream(input);
        this.addDiffReview(codeStream);
        this.removePromptInput();
      },
      onCancel: () => {
        console.debug('Prompt cancelled');
        inputContainer.remove();
        this.addCellActivateButton();
      }
    });

    const root = createRoot(inputContainer);
    root.render(inputComponent);
    this._notebookController.addElementAfterCellInput(
      this._cell,
      inputContainer
    );
  }

  public removePromptInput() {
    const inputContainer = this._cell.node.querySelector(
      '.jv-cell-ai-input-container'
    );
    if (inputContainer) {
      inputContainer.remove();
    }
  }

  public createCodeStream(prompt: string) {
    const codeStream = setupCodeGenerationStream({
      currentCell: this._cell,
      previousCells: this._notebookController.getPreviousCells(this._cell),
      nextCells: this._notebookController.getNextCells(this._cell),
      userInput: prompt,
      language: this._notebookController.getLanguage()
    });

    return codeStream;
  }

  public addDiffReview(codeStream: AsyncIterable<string>) {
    const cellNode = this._cell.node;
    const diffReviewContainer = document.createElement('div');
    const root = createRoot(diffReviewContainer);

    const diffReviewComponent = React.createElement(DiffReview, {
      activeCell: this._cell,
      oldCode: this._cell.model.sharedModel.source,
      generateCodeStream: codeStream,
      acceptCodeHandler: (code: string) => {
        this._notebookController.writeCodeInCell(this._cell, code);
        this.activate();
      },
      rejectCodeHandler: () => {
        this.activate();
      },
      editPromptHandler: (code: string) => {
        this._notebookController.writeCodeInCell(this._cell, code);
        this.addPromptInput();
      },
      acceptAndRunHandler: (code: string) => {
        this._notebookController.writeCodeInCell(this._cell, code);
        this._notebookController.runCell(this._cell);
        this.activate();
        this._notebookController.insertCell(
          this._notebookController.currentCellIndex + 1
        );
      }
    });
    root.render(diffReviewComponent);
    cellNode.appendChild(diffReviewContainer);
  }
}
