import React from 'react';
import { useState, useEffect } from 'react'
import Editor from 'react-simple-code-editor';
import { highlight, languages } from 'prismjs/components/prism-core';
import 'prismjs/components/prism-clike';
import 'prismjs/components/prism-javascript';
import 'prismjs/components/prism-python';
import 'prismjs/themes/prism.css'; //Example style, you can use another
import axios from 'axios';

import Button from '@mui/material/Button';

function App() {
  const [code, setCode] =useState(
    `Function A:\n  Function B`
  );
  const [svgUrl, setSvgUrl] = React.useState("");
  const [svg, setSvg] = React.useState("");

  function onRenderTriggered() {
      console.log(code)
    axios.post('http://localhost:3001/sketcher', {text: code})
        .then(function(response) {
            setSvg(response.data.svg);
        }).catch(function(exception) {
            console.log(exception);
        });
  }

  function onRenderButtonClicked() {
    onRenderTriggered();
  }

  function onKeyDown(e) {
    if (e.key == 'r' && e.ctrlKey) {
        onRenderTriggered()
    }
  }

  useEffect(() => {
    document.addEventListener('keydown', onKeyDown);
  }, []);

  return (
    <div style={{textAlign:"center"}}>
      <div style={{width: "50%", float: "left"}}>
          <Button onClick={onRenderButtonClicked} variant="contained" style={{margin: "10px"}}>Render It! (Ctrl + R)</Button>
          <div style={{
                border: "2px solid",
                margin: "10px"
            }}>
              <Editor
                value={code}
                onValueChange={code => setCode(code)}
                highlight={code => highlight(code, languages.python)}
                padding={10}
                style={{
                  fontFamily: '"Fira code", "Fira Mono", monospace',
                  fontSize: 12,
                }}
              />
          </div>
      </div>
      <div style={{width: "50%", float: "left"}}>
            <span dangerouslySetInnerHTML={{__html: svg}} />
      </div>
    </div>
  );
}

export default App;
