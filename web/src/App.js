import React from 'react';
import { useState, useEffect, useRef } from 'react'
import axios from 'axios';
import Editor from '@monaco-editor/react';
import { Box, CssBaseline, AppBar, Toolbar, Typography, Backdrop, CircularProgress } from '@mui/material';
import { Button, ButtonGroup, FormControlLabel, Switch, TextField } from '@mui/material';
import { Modal, List, ListItem, ListItemButton , ListItemIcon, ListItemText } from '@mui/material';
import { Menu, MenuItem } from '@mui/material';
import CodeIcon from '@mui/icons-material/Code';
import AccountTreeIcon from '@mui/icons-material/AccountTree';
import ExploreOutlinedIcon from '@mui/icons-material/ExploreOutlined';
import ArticleIcon from '@mui/icons-material/Article';
import ModeEditIcon from '@mui/icons-material/ModeEdit';
import CheckIcon from '@mui/icons-material/Check';
import DownloadIcon from '@mui/icons-material/Download';

var saveScheduled = false;
var stateBeforeRenaming = {}
var filename = "hello.he";

const hostname = window.location.protocol + "//" + window.location.hostname;
const portnum = 3001; 
const apipath = hostname + ":" + portnum;

function App() {
    const editorRef = useRef(null);
    const [editorEditable, setEditorEditable] = React.useState(false);
    const initialCode = "";
    const [displayedFilename, setDisplayedFilename] = React.useState(filename);
    const [svgUrl, setSvgUrl] = React.useState("");
    const [svg, setSvg] = React.useState("");
    const [autoRefreshSwitch, setAutoRefreshSwitch] = React.useState(true);
    const [saveButtonEnabled, setSaveButtonEnabled] = React.useState(false);
    const [fileSelectorOpened, setFileSelectorOpened] = React.useState(false);
    const [fileSelectorList, setFileSelectorList] = React.useState([]);
    const [renamingFilename, setRenamingFilename] = React.useState(false);
    const [nowLoading, setNowLoading] = React.useState(true);
    const [contextMenu, setContextMenu] = React.useState(null);

    function handleEditorDidMount(editor, monaco) {
        editorRef.current = editor;
        setTimeout(() => {
            loadCurrentFile();
            refreshDiagram();
            changeAutoRefresh(true);
        }, 1000);
    }

    function refreshDiagram() {
        var code = editorRef.current.getValue();
        axios.post(apipath + '/sketcher', {text: code})
            .then(function(response) {
                setSvg(response.data.svg);
                }).catch(function(exception) {
                    console.log(exception);
                    });
    }

    function startRenaming() {
        stateBeforeRenaming = {
            saveScheduled: saveScheduled,
            filename: filename
        };
        saveScheduled = false;
        setRenamingFilename(true);
        setEditorEditable(false);
    }

    function finishRenaming() {
        var recoverState = () => {
            setEditorEditable(true);
            setRenamingFilename(false);
        };
        if (!filename.endsWith('.he')) {
            alert("File name should ends with '.he'.");
            return;
        }
        if (stateBeforeRenaming.filename == filename) {
            recoverState();
        } else {
            saveCurrentFile(() => {
                deleteFile(stateBeforeRenaming.filename,
                    () => {
                    recoverState();
                });
            });
        }
    }
    
    function saveWatcher() {
        if (saveScheduled) {
            saveCurrentFile();
        }
    }

    function onSaveButtonClicked() {
        saveCurrentFile();
    }

    function loadCurrentFile(postFunction) {
        console.log("load from " + filename);
        setEditorEditable(false);
        setNowLoading(true);
        axios.get(apipath + '/workspace/' + filename)
            .then(function(response) {
                    saveScheduled = false;
                    editorRef.current.setValue(response.data);
                    setSaveButtonEnabled(false);
                    setNowLoading(false);
                    setEditorEditable(true);
                    if (postFunction)
                        postFunction();
                    }).catch(function(exception) {
                        console.log(exception);
                        setNowLoading(false);
                        setEditorEditable(true);
                        if (postFunction)
                            postFunction();
                        });
    }

    function saveCurrentFile(postFunction) {
        console.log("save to " + filename);
        var code = editorRef.current.getValue();
        saveScheduled = false;
        axios.post(apipath + '/workspace/' + filename, {text: code})
            .then(function(response) {
                if (response.data.isSuccess) {
                    setSaveButtonEnabled(false);
                    if (postFunction)
                        postFunction();
                } else {
                    saveScheduled = true;
                    console.log(response.data.message);
                }
                }).catch(function(exception) {
                    saveScheduled = true;
                    console.log(exception);
                    });
    }

    function deleteFile(targetFilename, postFunction) {
        console.log("delete " + targetFilename);
        var code = editorRef.current.getValue();
        saveScheduled = false;
        axios.delete(apipath + '/workspace/' + targetFilename)
            .then(function(response) {
                if (response.data.isSuccess) {
                    if (postFunction)
                        postFunction();
                } else {
                    console.log(response.data.message);
                    if (postFunction)
                        postFunction();
                }
                }).catch(function(exception) {
                    console.log(exception);
                    if (postFunction)
                        postFunction();
                    });
    }

    const downloadFile = (url, filename) => {
        fetch(url, { method: 'GET' })
            .then((res) => { return res.blob(); })
            .then((blob) => {
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = filename;
                document.body.appendChild(a);
                a.click();
                setTimeout((_) => { window.URL.revokeObjectURL(url); }, 60000);
                a.remove();
            })
            .catch((err) => { console.error('err: ', err); });
    };

    const downloadRenderedFile = (filetype) => {
        const extension = '.' + filetype;
        const url = apipath + '/to_' + filetype + '/' + filename;
        var rendered_filename = filename;
        if (!rendered_filename.endsWith('.png')) {
            if (rendered_filename.endsWith('.he')) {
                rendered_filename = rendered_filename.replace('.he', extension);
            } else {
                rendered_filename += extension;
            }
        }
        downloadFile(url, rendered_filename);
    }

    function onDownloadHeClicked() {
        downloadFile(apipath + '/workspace/' + filename, filename);
    }

    function onDownloadPngClicked() {
        downloadRenderedFile('png');
    }

    function onDownloadSvgClicked() {
        downloadRenderedFile('svg');
    }

    function onFileItemClicked(fileItem) {
        setFileSelectorOpened(false);
        saveCurrentFile(() => {
            filename = fileItem;
            setDisplayedFilename(filename);
            loadCurrentFile();
        });
    }

    function onNewFileButtonClicked() {
        axios.post(apipath + '/workspace')
            .then(function(response) {
                    filename = response.data.filename;
                    setDisplayedFilename(filename);
                    loadCurrentFile(() => {
                        startRenaming();
                        }).catch(function(exception) {
                            console.log(exception);
                            alert(exception);
                            });
                    });
    }

    function onSelectFileButtonClicked() {
        setFileSelectorOpened(true);
        updateFileSelectorList();
    }

    function updateFileSelectorList(postFunction) {
        axios.get(apipath + '/workspace')
            .then(function(response) {
                    setFileSelectorList(response.data.files);
                    if (postFunction)
                        postFunction();
                    }).catch(function(exception) {
                        console.log(exception);
                        if (postFunction)
                            postFunction();
                        });
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
        setSaveButtonEnabled(true);
        saveScheduled = true;
        if (autoRefreshSwitch)
            refreshDiagram();
    }

    function handleContextMenu(event, menuItemFilename) {
        console.log(filename);
        event.preventDefault();
        const deleteEnabled = (filename != menuItemFilename);
        setContextMenu(contextMenu === null ?
            {
                mouseX: event.clientX + 2,
                mouseY: event.clientY - 6,
                filename: menuItemFilename,
                deleteEnabled: deleteEnabled
            } : null, );
    }

    function onContextMenuClose() {
        setContextMenu(null);
    }

    function onDeleteContextMenuItemClicked() {
        deleteFile(contextMenu.filename, () => {
                updateFileSelectorList(() => {
                    onContextMenuClose();
                });
        });
    }

    useEffect(() => {
            document.addEventListener('keydown', onKeyDown);
            setInterval(() => {saveWatcher();}, 2000);
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
        ['New File', 'newFile', onNewFileButtonClicked],
        ['Select File', 'selectFile', onSelectFileButtonClicked],
    ]

    return (
        <>
        <Box sx={{ display: 'flex' }}>
            <CssBaseline />
            <AppBar component="nav">
                <Toolbar>
                    <Typography variant="h4" style={{marginRight:"20px"}}>HawkEye</Typography>
                    <Button key="save"
                        color="inherit" variant="outlined" disabled={!saveButtonEnabled} style={{marginRight:"20px"}}
                        onClick={onSaveButtonClicked}
                        >
                        {(saveButtonEnabled) ? "Save" : "Saved"}
                    </Button>
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
                        {(renamingFilename) ?
                            <>
                                <TextField id="outlined-basic" variant="outlined" size="small" value={displayedFilename} sx={{width: "80%"}}
                                    onChange={(e) => { filename = e.target.value; setDisplayedFilename(filename); }}/>
                            </> :
                            <>{displayedFilename}
                           </>}
                    </Typography>
                    <ButtonGroup variant="contained" sx={{marginTop: '5px'}}>
                        {(renamingFilename) ?
                        <Button key="confirmFilenameButton" size="small"
                            onClick={() => { finishRenaming(); }}>
                            <CheckIcon style={{marginRight:"5px"}} /> Confirm File Name
                        </Button> :
                        <Button key="editFilenameButton" size="small"
                            onClick={() => { startRenaming(); }}>
                            <ModeEditIcon style={{marginRight:"5px"}} /> Rename
                        </Button>}
                        <Button key="downloadSketchFileButton" size="small"
                            onClick={() => { onDownloadHeClicked(); }}>
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
                        onChange={onEditorChange} options={{readOnly: !editorEditable}}/>
                    </div>
                </div>
                <div style={{width: "50%", textAlign:"left", float: "left", textAlign:'left'}}>
                    <div style={{width: "100%"}}>
                        <Typography noWrap variant="h4">
                            <AccountTreeIcon sx={{fontSize: 28, marginRight: '5px'}} />
                            Diagram
                        </Typography>
                        <ButtonGroup variant="contained" sx={{marginTop: '5px'}}>
                            <Button key="downloadDiagramPNGFileButton" size="small"
                                onClick={() => { onDownloadPngClicked(); }}>
                                <DownloadIcon style={{marginRight:"5px"}} /> Download (png)
                            </Button>
                            <Button key="downloadDiagramSVGFileButton" size="small"
                                onClick={() => { onDownloadSvgClicked(); }}>
                                <DownloadIcon style={{marginRight:"5px"}} /> Download (svg)
                            </Button>
                        </ButtonGroup>
                    </div>
                    <div style={{overflowX: "scroll", overflowY: "scroll", width: "100%", height: "80vh"}}>
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
                {fileSelectorList.map((fileItem) => 
                    <ListItem disablePadding>
                        <ListItemButton onClick={() => { onFileItemClicked(fileItem) }}
                            onContextMenu={(e) => {handleContextMenu(e, fileItem); }}>
                            <ListItemIcon><ArticleIcon /></ListItemIcon>
                            <ListItemText primary={fileItem} />
                        </ListItemButton>
                    </ListItem>
                )}
            </List>
          </Box>
        </Modal>
        <Menu open={contextMenu != null}
            onClose={onContextMenuClose}
            anchorReference="anchorPosition"
            anchorPosition={contextMenu !== null ? { top: contextMenu.mouseY, left: contextMenu.mouseX } : undefined} >
            <MenuItem disabled={contextMenu !== null ? !contextMenu.deleteEnabled : true} onClick={onDeleteContextMenuItemClicked}>Delete</MenuItem>
        </Menu>
        <Backdrop sx={{ color: '#fff', zIndex: (theme) => theme.zIndex.drawer + 1 }}
            open={nowLoading}>
                <CircularProgress color="inherit" />
        </Backdrop>
      </>
    );
    }

export default App;
