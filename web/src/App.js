import React from 'react';
import Editor from 'react-simple-code-editor';
import { highlight, languages } from 'prismjs/components/prism-core';
import 'prismjs/components/prism-clike';
import 'prismjs/components/prism-javascript';
import 'prismjs/themes/prism.css'; //Example style, you can use another
import { usePython } from 'react-py'

import Button from '@mui/material/Button';

function App() {
  const { runPython, stdout, stderr, isLoading, isRunning } = usePython()
  const [code, setCode] = React.useState(
    `function add(a, b) {\n  return a + b;\n}`
  );

  function onRunButtonClicked() {
  }

  return (
    <div style={{textAlign:"center"}}>
      <Editor
        value={code}
        onValueChange={code => setCode(code)}
        highlight={code => highlight(code, languages.js)}
        padding={10}
        style={{
          fontFamily: '"Fira code", "Fira Mono", monospace',
          fontSize: 12,
        }}
      />
      <Button onclick={onRunButtonClicked} variant="contained">Run</Button>
    </div>
  );
}

export default App;
