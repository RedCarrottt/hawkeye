import React from 'react';
import { useState } from 'react'
import Editor from 'react-simple-code-editor';
import { highlight, languages } from 'prismjs/components/prism-core';
import 'prismjs/components/prism-clike';
import 'prismjs/components/prism-javascript';
import 'prismjs/themes/prism.css'; //Example style, you can use another
import axios from 'axios';

import Button from '@mui/material/Button';

function App() {
  const [code, setCode] =useState(
    `Function A:\n  Function B`
  );
  const [svgUrl, setSvgUrl] = React.useState("");

  function onRunButtonClicked() {
    axios.post('http://localhost:3001/sketcher', {text: code})
        .then(function(response) {
            setSvgUrl(response.data.url + "?" + performance.now());
        }).catch(function(exception) {
            console.log(exception);
        });
  }

  return (
    <div style={{textAlign:"center"}}>
      <div>
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
      <Button onClick={onRunButtonClicked} variant="contained">Run</Button>
      <img src={svgUrl} />
      </div>
    </div>
  );
}

export default App;
