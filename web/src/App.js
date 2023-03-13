import React from 'react';
import { useState, useEffect, useRef } from 'react'
import axios from 'axios';
import Editor from '@monaco-editor/react';
import { Box, CssBaseline, AppBar, Button, Typography, Toolbar } from '@mui/material';
import CodeIcon from '@mui/icons-material/Code';
import AccountTreeIcon from '@mui/icons-material/AccountTree';

function App() {
    const editorRef = useRef(null);
    const initialCode = "Function A:\n  Function B";
    const [svgUrl, setSvgUrl] = React.useState("");
    const [svg, setSvg] = React.useState("");

    function handleEditorDidMount(editor, monaco) {
        editorRef.current = editor;
        setTimeout(onRenderTriggered(), 2000);
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

    function onFileListButtonClicked() {
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

    const [anchorElNav, setAnchorElNav] = React.useState(null);
    const [anchorElUser, setAnchorElUser] = React.useState(null);

    const handleOpenNavMenu = (event) => {
        setAnchorElNav(event.currentTarget);
    };
    const handleOpenUserMenu = (event) => {
        setAnchorElUser(event.currentTarget);
    };

    const handleCloseNavMenu = () => {
        setAnchorElNav(null);
    };

    const handleCloseUserMenu = () => {
        setAnchorElUser(null);
    };

    const menuItems = [
        ['File List', 'fileList', onFileListButtonClicked],
        ['Render (Ctrl + R)', 'render', onRenderButtonClicked]
    ]

    return (
        <Box sx={{ display: 'flex' }}>
            <CssBaseline />
            <AppBar component="nav">
                <Toolbar>
                    {menuItems.map((menuItem) => 
                        <Button key={menuItem[1]} 
                            color="inherit" variant="outlined" style={{marginRight:"10px"}}
                            onClick={menuItem[2]}>
                            {menuItem[0]}
                        </Button>
                    )}
                </Toolbar>
            </AppBar>
            <Box sx={{ display: { xs: 'none', sm: 'block', width: "100%", textAlign:'center', margin: "10px"} }}>
                <Toolbar />
                <div style={{width: "50%", float: "left", textAlign:'left'}}>
                    <Typography variant="h4"><CodeIcon /> Sketch Editor</Typography>
                    <div style={{
                        border: "2px solid",
                        margin: "10px"}}>
                        <Editor
                        defaultValue={initialCode} defaultLanguage="python"
                        height="80vh"
                        onMount={handleEditorDidMount} />
                    </div>
                </div>
                <div style={{width: "50%", textAlign:"left", float: "left", textAlign:'left'}}>
                    <Typography variant="h4"><AccountTreeIcon /> Results</Typography>
                    <span dangerouslySetInnerHTML={{__html: svg}} />
                </div>
            </Box>
        </Box>
    );
    }

export default App;
