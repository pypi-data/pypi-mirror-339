import React, { useState, useEffect, useRef } from 'react';
import { EditorView } from '@codemirror/view';
import { CodeMirrorEditor } from '@jupyterlab/codemirror';
import { EditorState, Extension } from '@codemirror/state';
import { unifiedMergeView } from '@codemirror/merge';
import { python } from '@codemirror/lang-python';
import { highlightSpecialChars } from '@codemirror/view';
import { jupyterTheme } from '@jupyterlab/codemirror';
import { Cell } from '@jupyterlab/cells';
import { ButtonsContainer } from './DiffReviewButtons';

function applyDiffToEditor(
  editor: CodeMirrorEditor,
  original: string,
  modified: string,
  isNewCodeGeneration = false
): EditorView {
  // This function
  const extensions: Extension[] = [
    python(),
    jupyterTheme,
    EditorView.editable.of(false),
    EditorState.readOnly.of(true),
    highlightSpecialChars()
  ];

  if (!isNewCodeGeneration) {
    extensions.push(
      unifiedMergeView({
        original: original,
        mergeControls: false,
        gutter: false
      })
    );
  }
  // Create a new EditorView with the diff content
  const newView = new EditorView({
    state: EditorState.create({
      doc: modified,
      extensions: extensions
    }),
    parent: editor.editor.dom
  });

  // Hide the original editor view
  editor.editor.dom.classList.add('hidden-editor');

  // Add a class for new code generation
  if (isNewCodeGeneration) {
    newView.dom.classList.add('new-code-generation');
  }

  // add a streaming-now class to the new view
  newView.dom.classList.add('streaming-now');
  // Append the new view to the same parent as the original editor
  editor.host.appendChild(newView.dom);
  return newView;
}

interface IDiffReviewProps {
  activeCell: Cell;
  oldCode: string;
  generateCodeStream: AsyncIterable<string>; // Fixed type definition
  acceptCodeHandler: (code: string) => void;
  rejectCodeHandler: () => void;
  editPromptHandler: (code: string) => void;
  acceptAndRunHandler: (code: string) => void;
}

export const DiffReview: React.FC<IDiffReviewProps> = ({
  activeCell,
  oldCode,
  generateCodeStream,
  acceptCodeHandler,
  rejectCodeHandler,
  editPromptHandler,
  acceptAndRunHandler
}) => {
  const [diffView, setDiffView] = useState<EditorView | null>(null);
  const [stream, setStream] = useState<AsyncIterable<string> | null>(null);
  const [newCode, setNewCode] = useState<string>('');
  const [streamingDone, setStreamingDone] = useState<boolean>(false);
  const [statusText, setStatusText] = useState<string>('Generating code...');
  const buttonsRef = useRef<HTMLDivElement>(null);
  // Create the diff view once the active cell and old code are available.
  useEffect(() => {
    if (activeCell && oldCode !== undefined) {
      const editor = activeCell.editor as CodeMirrorEditor;
      const initialDiffView = applyDiffToEditor(
        editor,
        oldCode,
        oldCode,
        oldCode.trim() === '' // flag for new code generation
      );
      setDiffView(initialDiffView);
    }
  }, [activeCell, oldCode]);

  // Start the code generation stream.
  useEffect(() => {
    const initiateStream = async () => {
      try {
        const codeStream = generateCodeStream;
        setStream(codeStream);
      } catch (error: any) {
        console.error('Error generating code stream:', error);
        setStatusText('Error generating code.');
        setStreamingDone(true);
      }
    };
    initiateStream();
  }, [generateCodeStream]);

  // Accumulate code from the stream.
  useEffect(() => {
    if (stream) {
      const accumulate = async () => {
        try {
          for await (const chunk of stream) {
            setNewCode(prevCode => prevCode + chunk);
          }
          setStreamingDone(true);
          setStatusText('');
        } catch (error) {
          console.error('Error processing stream:', error);
          setStreamingDone(true);
          setStatusText('');
        }
      };
      accumulate();
    }
  }, [stream]);

  // When streaming is complete, finalize the diff view by applying fixed code.
  useEffect(() => {
    if (streamingDone && diffView) {
      diffView.dom.classList.remove('streaming-now');
      diffView.dispatch({
        changes: {
          from: 0,
          to: diffView.state.doc.length,
          insert: newCode
        }
      });
    }
  }, [streamingDone, diffView, newCode]);

  // when streming is done, scroll the button container into view
  useEffect(() => {
    if (streamingDone && buttonsRef.current) {
      buttonsRef.current.scrollIntoView({
        behavior: 'smooth',
        block: 'center'
      });
    }
  }, [streamingDone]);

  // Continuously update the diff view while new code arrives.
  useEffect(() => {
    if (!streamingDone && activeCell && diffView) {
      const oldCodeLines = oldCode.split('\n');
      const newCodeLines = newCode.split('\n');
      if (newCodeLines.length > 1) {
        let diffCode = '';
        if (newCodeLines.length < oldCodeLines.length) {
          diffCode = [
            ...newCodeLines.slice(0, -1),
            oldCodeLines[newCodeLines.length - 1] + '\u200B',
            ...oldCodeLines.slice(newCodeLines.length)
          ].join('\n');
        } else {
          diffCode = newCode.split('\n').slice(0, -1).join('\n');
        }
        diffView.dispatch({
          changes: {
            from: 0,
            to: diffView.state.doc.length,
            insert: diffCode
          }
        });
        // Optionally, mark the last changed line.
        const changedLines = diffView.dom.querySelectorAll('.cm-changedLine');
        if (changedLines.length > 0) {
          changedLines[
            changedLines.length - 1
          ].previousElementSibling?.classList.add('hidden-diff');
        }
      }
    }
  }, [newCode, streamingDone, activeCell, diffView, oldCode]);

  const cleanUp = () => {
    // remove the diff review and restore the original editor
    const diffReviewContainer = diffView?.dom;
    if (diffReviewContainer) {
      diffReviewContainer.remove();
    }
    const editor = activeCell.editor as CodeMirrorEditor;
    editor.editor.dom.classList.remove('hidden-editor');
    // remove the buttons container
    const buttonsContainer = buttonsRef.current;
    if (buttonsContainer) {
      buttonsContainer.remove();
    }
  };

  const onAcceptAndRun = () => {
    acceptAndRunHandler(newCode);
    cleanUp();
  };

  const onAccept = () => {
    acceptCodeHandler(newCode);
    cleanUp();
  };

  const onReject = () => {
    rejectCodeHandler();
    cleanUp();
  };

  const onEditPrompt = () => {
    editPromptHandler(newCode);
    cleanUp();
  };

  return (
    <div>
      {statusText && <p className="status-element">{statusText}</p>}
      {diffView && streamingDone && (
        <ButtonsContainer
          buttonsRef={buttonsRef}
          onAcceptAndRun={onAcceptAndRun}
          onAccept={onAccept}
          onReject={onReject}
          onEditPrompt={onEditPrompt}
        />
      )}
    </div>
  );
};
