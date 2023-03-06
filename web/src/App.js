import React from 'react';
import { useState, useEffect, useRef } from 'react'
import axios from 'axios';
import Button from '@mui/material/Button';
import Editor from '@monaco-editor/react';

function App() {
    const editorRef = useRef(null);
    const initialCode = "Function A:\n  Function B";
    const [svgUrl, setSvgUrl] = React.useState("");
    const [svg, setSvg] = React.useState("");

    function handleEditorDidMount(editor, monaco) {
        editorRef.current = editor;
    }

    function onRenderTriggered() {
        var code = editorRef.current.getValue();
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
                <Button onClick={onRenderButtonClicked}
                    variant="contained"
                    style={{margin: "10px"}}>
                    Render It! (Ctrl + R)
                </Button>
                <div style={{
                    border: "2px solid",
                    margin: "10px"}}>
                    <Editor
                    defaultValue={initialCode} defaultLanguage="python"
                    height="90vh"
                    onMount={handleEditorDidMount} />
                </div>
            </div>
            <div style={{width: "50%", float: "left"}}>
                <span dangerouslySetInnerHTML={{__html: svg}} />
            </div>
        </div>
    );
    }

export default App;
