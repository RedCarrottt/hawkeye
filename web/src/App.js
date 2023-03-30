import React from 'react';
import { useState, useEffect, useRef } from 'react'
import axios from 'axios';
import Editor from '@monaco-editor/react';
import { Box, CssBaseline, AppBar, Toolbar, Typography } from '@mui/material';
import { Button, ButtonGroup, FormControlLabel, Switch, TextField } from '@mui/material';
import { Modal, List, ListItem, ListItemButton , ListItemIcon, ListItemText } from '@mui/material';
import CodeIcon from '@mui/icons-material/Code';
import AccountTreeIcon from '@mui/icons-material/AccountTree';
import ExploreOutlinedIcon from '@mui/icons-material/ExploreOutlined';
import ArticleIcon from '@mui/icons-material/Article';
import ModeEditIcon from '@mui/icons-material/ModeEdit';
import CheckIcon from '@mui/icons-material/Check';
import DownloadIcon from '@mui/icons-material/Download';

function App() {
    const editorRef = useRef(null);
    const initialCode = "Function A:\n  Function B";
    const [svgUrl, setSvgUrl] = React.useState("");
    const [svg, setSvg] = React.useState("");
    const [autoRefreshSwitch, setAutoRefreshSwitch] = React.useState(true);
    const [fileSelectorOpened, setFileSelectorOpened] = React.useState(false);
    const [filename, setFilename] = React.useState("hello.he");
    const [editingFilename, setEditingFilename] = React.useState(false);

    function handleEditorDidMount(editor, monaco) {
        editorRef.current = editor;
        setTimeout(() => {
            refreshDiagram();
            changeAutoRefresh(true);
        }, 2000);
    }

    function refreshDiagram() {
        var code = editorRef.current.getValue();
        console.log(code)
            axios.post('http://localhost:3001/sketcher', {text: code})
            .then(function(response) {
                    setSvg(response.data.svg);
                    }).catch(function(exception) {
                        console.log(exception);
                        });
    }

    function onFileItemClicked() {
        // TODO: select file
        setFileSelectorOpened(false);
    }

    function onSelectFileButtonClicked() {
        setFileSelectorOpened(true);
    }
    function onCloseFileSelector() {
        setFileSelectorOpened(false);
    }

    function onKeyDown(e) {
        // TODO:
    }

    function onAutoRefreshSwitchChange(e) {
        changeAutoRefresh(e.target.checked);
    }

    function changeAutoRefresh(isEnable) {
        if (isEnable)
            refreshDiagram();
        setAutoRefreshSwitch(isEnable);
    }

    function onEditorChange() {
        if (autoRefreshSwitch)
            refreshDiagram();
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
        ['Select File', 'selectFile', onSelectFileButtonClicked],
    ]

    const fileList = [
        "File A",
        "File B",
        "File C"
    ]

    return (
        <>
        <Box sx={{ display: 'flex' }}>
            <CssBaseline />
            <AppBar component="nav">
                <Toolbar>
                    <Typography variant="h4" style={{marginRight:"20px"}}>HawkEye</Typography>
                    {menuItems.map((menuItem) => 
                        <Button key={menuItem[1]} 
                            color="inherit" variant="outlined" style={{marginRight:"20px"}}
                            onClick={menuItem[2]}>
                            {menuItem[0]}
                        </Button>
                    )}
                    <FormControlLabel control={
                        <Switch defaultChecked color="warning" checked={autoRefreshSwitch} onChange={onAutoRefreshSwitchChange} />
                        } label="Auto-Refresh" />
                </Toolbar>
            </AppBar>
            <Box sx={{ display: { xs: 'none', sm: 'block', width: "100%", textAlign:'center', margin: "10px"} }}>
                <Toolbar />
                <div style={{width: "50%", float: "left", textAlign:'left'}}>
                    <Typography noWrap variant="h4">
                        <ArticleIcon sx={{fontSize: 28, marginRight: '5px'}} />
                        {(editingFilename) ?
                            <>
                                <TextField id="outlined-basic" variant="outlined" size="small" value={filename} sx={{width: "80%"}}
                                    onChange={(e) => { setFilename(e.target.value); }}/>
                            </> :
                            <>{filename}
                           </>}
                    </Typography>
                    <ButtonGroup variant="contained" sx={{marginTop: '5px'}}>
                        {(editingFilename) ?
                        <Button key="confirmFilenameButton" size="small"
                            onClick={() => { setEditingFilename(false); }}>
                            <CheckIcon style={{marginRight:"5px"}} /> Confirm File Name
                        </Button> :
                        <Button key="editFilenameButton" size="small"
                            onClick={() => { setEditingFilename(true); }}>
                            <ModeEditIcon style={{marginRight:"5px"}} /> Rename
                        </Button>}
                        <Button key="downloadSketchFileButton" size="small">
                            <DownloadIcon style={{marginRight:"5px"}} /> Download (he)
                        </Button>
                    </ButtonGroup>
                    <div style={{
                        border: "2px solid",
                        margin: "10px"}}>
                        <Editor
                        defaultValue={initialCode} defaultLanguage="python"
                        height="80vh"
                        onMount={handleEditorDidMount}
                        onChange={onEditorChange} />
                    </div>
                </div>
                <div style={{width: "50%", textAlign:"left", float: "left", textAlign:'left'}}>
                    <div style={{width: "100%"}}>
                        <Typography noWrap variant="h4">
                            <AccountTreeIcon sx={{fontSize: 28, marginRight: '5px'}} />
                            Diagram
                        </Typography>
                        <ButtonGroup variant="contained" sx={{marginTop: '5px'}}>
                            <Button key="downloadDiagramPNGFileButton" size="small">
                                <DownloadIcon style={{marginRight:"5px"}} /> Download (png)
                            </Button>
                            <Button key="downloadDiagramSVGFileButton" size="small">
                                <DownloadIcon style={{marginRight:"5px"}} /> Download (svg)
                            </Button>
                        </ButtonGroup>
                    </div>
                    <div style={{overflowX: "scroll", overflowY: "scroll", width: "600px", height: "1024px"}}>
                        <span dangerouslySetInnerHTML={{__html: svg}} />
                    </div>
                </div>
            </Box>
        </Box>
        <Modal
          open={fileSelectorOpened}
          onClose={onCloseFileSelector}
          aria-labelledby="file-selector-title"
          aria-describedby="file-selector-description" >
          <Box sx={{position: 'absolute', top: '50%', left: '50%',
              transform: 'translate(-50%, -50%)', width: '80%', height: '50%',
              bgcolor: 'background.paper', border: '2px solid #000',
              boxShadow: 24, p: 4,
          }}>
            <Typography id="file-selector-title" variant="h4">
                <ExploreOutlinedIcon sx={{fontSize: 28}} /> File Selector
            </Typography>
            <List id="file-selector-description" sx={{ mt: 2 }}>
                {fileList.map((fileItem) => 
                    <ListItem disablePadding>
                        <ListItemButton onClick={onFileItemClicked}>
                            <ListItemIcon><ArticleIcon /></ListItemIcon>
                            <ListItemText primary={fileItem} />
                        </ListItemButton>
                    </ListItem>
                )}
            </List>
          </Box>
        </Modal>
      </>
    );
    }

export default App;
