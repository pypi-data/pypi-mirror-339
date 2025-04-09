"use strict";
(self["webpackChunkvariable_inspector"] = self["webpackChunkvariable_inspector"] || []).push([["lib_index_js"],{

/***/ "./lib/components/paginationControls.js":
/*!**********************************************!*\
  !*** ./lib/components/paginationControls.js ***!
  \**********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   PaginationControls: () => (/* binding */ PaginationControls)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _icons_skipLeftIcon__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../icons/skipLeftIcon */ "./lib/icons/skipLeftIcon.js");
/* harmony import */ var _icons_smallSkipLeftIcon__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../icons/smallSkipLeftIcon */ "./lib/icons/smallSkipLeftIcon.js");
/* harmony import */ var _icons_smallSkipRightIcon__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../icons/smallSkipRightIcon */ "./lib/icons/smallSkipRightIcon.js");
/* harmony import */ var _icons_skipRightIcon__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../icons/skipRightIcon */ "./lib/icons/skipRightIcon.js");





const PaginationControls = ({ rowsCount, colsCount, rowInput, setRowInput, currentRow, setCurrentRow, columnInput, setColumnInput, currentColumn, setCurrentColumn, cellRowInput, setCellRowInput, cellColumnInput, setCellColumnInput, handleGotoCell, handlePrevRowPage, handleNextRowPage, handlePrevColumnPage, handleNextColumnPage }) => {
    return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: "mljar-variable-inspector-pagination-container" },
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: "mljar-variable-inspector-pagination-item" },
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: "mljar-variable-inspector-choose-range" },
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement("span", null, "Rows from "),
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement("button", { onClick: e => handlePrevRowPage('first'), className: "mljar-variable-inspector-skip-button", title: 'Display first 100 rows' },
                    react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_icons_skipLeftIcon__WEBPACK_IMPORTED_MODULE_1__.skipLeftIcon.react, { className: "mljar-variable-inspector-skip-icon" })),
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement("button", { onClick: e => handlePrevRowPage('previous'), className: "mljar-variable-inspector-skip-button", title: 'Display previous 100 rows' },
                    react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_icons_smallSkipLeftIcon__WEBPACK_IMPORTED_MODULE_2__.smallSkipLeftIcon.react, { className: "mljar-variable-inspector-skip-icon" })),
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement("input", { title: 'Start with row', type: "number", min: 0, max: rowsCount - 1, value: rowInput === '' ? (rowInput = '0') : rowInput, className: "mljar-variable-inspector-pagination-input", onChange: e => setRowInput(e.target.value), onKeyDown: e => {
                        if (e.key === 'Enter') {
                            const newPage = parseInt(rowInput, 10);
                            if (!isNaN(newPage) && newPage >= 0 && newPage <= rowsCount) {
                                setCurrentRow(newPage);
                                setRowInput(newPage.toString());
                            }
                        }
                    }, onBlur: () => {
                        const newPage = parseInt(rowInput, 10);
                        if (isNaN(newPage) || newPage < 0 || newPage > rowsCount) {
                            setRowInput(currentRow.toString());
                        }
                        else {
                            setCurrentRow(newPage);
                        }
                    } }),
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement("span", null, "to "),
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement("span", null, parseInt(rowInput) + 99 >= rowsCount
                    ? rowsCount - 1
                    : parseInt(rowInput) + 99),
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement("button", { onClick: e => handleNextRowPage('next'), className: "mljar-variable-inspector-skip-button", title: 'Display next 100 rows' },
                    react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_icons_smallSkipRightIcon__WEBPACK_IMPORTED_MODULE_3__.smallSkipRightIcon.react, { className: "mljar-variable-inspector-skip-icon" })),
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement("button", { onClick: e => handleNextRowPage('last'), className: "mljar-variable-inspector-skip-button", title: 'Display last 100 rows' },
                    react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_icons_skipRightIcon__WEBPACK_IMPORTED_MODULE_4__.skipRightIcon.react, { className: "mljar-variable-inspector-skip-icon" })),
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement("span", null,
                    "Total ",
                    react__WEBPACK_IMPORTED_MODULE_0___default().createElement("span", { style: { fontWeight: 600 } }, rowsCount),
                    " rows")),
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: "mljar-variable-inspector-choose-range" },
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement("span", null, "Columns from "),
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement("button", { onClick: e => handlePrevColumnPage('first'), className: "mljar-variable-inspector-skip-button", title: 'Display first 50 columns' },
                    react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_icons_skipLeftIcon__WEBPACK_IMPORTED_MODULE_1__.skipLeftIcon.react, { className: "mljar-variable-inspector-skip-icon" })),
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement("button", { onClick: e => handlePrevColumnPage('previous'), className: "mljar-variable-inspector-skip-button", title: 'Display previous 50 columns' },
                    react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_icons_smallSkipLeftIcon__WEBPACK_IMPORTED_MODULE_2__.smallSkipLeftIcon.react, { className: "mljar-variable-inspector-skip-icon" })),
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement("input", { title: 'Start with column', type: "number", min: 0, max: colsCount - 1, value: columnInput === '' ? (columnInput = '0') : columnInput, className: "mljar-variable-inspector-pagination-input", onChange: e => setColumnInput(e.target.value), onKeyDown: e => {
                        if (e.key === 'Enter') {
                            const newPage = parseInt(columnInput, 10);
                            if (!isNaN(newPage) && newPage >= 0 && newPage <= colsCount) {
                                setCurrentColumn(newPage);
                                setColumnInput(newPage.toString());
                            }
                        }
                    }, onBlur: () => {
                        const newPage = parseInt(columnInput, 10);
                        if (isNaN(newPage) || newPage < 0 || newPage > colsCount) {
                            setColumnInput(currentColumn.toString());
                        }
                        else {
                            setCurrentColumn(newPage);
                        }
                    } }),
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement("span", null, "to "),
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement("span", null, parseInt(columnInput) + 49 >= colsCount
                    ? colsCount - 1
                    : parseInt(columnInput) + 49),
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement("button", { onClick: e => handleNextColumnPage('next'), className: "mljar-variable-inspector-skip-button", title: 'Display next 50 columns' },
                    react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_icons_smallSkipRightIcon__WEBPACK_IMPORTED_MODULE_3__.smallSkipRightIcon.react, { className: "mljar-variable-inspector-skip-icon" })),
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement("button", { onClick: e => handleNextColumnPage('last'), className: "mljar-variable-inspector-skip-button", title: 'Display last 50 columns' },
                    react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_icons_skipRightIcon__WEBPACK_IMPORTED_MODULE_4__.skipRightIcon.react, { className: "mljar-variable-inspector-skip-icon" })),
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement("span", null,
                    "Total ",
                    react__WEBPACK_IMPORTED_MODULE_0___default().createElement("span", { style: { fontWeight: 600 } }, colsCount),
                    " columns")))));
};


/***/ }),

/***/ "./lib/components/searchBar.js":
/*!*************************************!*\
  !*** ./lib/components/searchBar.js ***!
  \*************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   SearchBar: () => (/* binding */ SearchBar)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _context_notebookVariableContext__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../context/notebookVariableContext */ "./lib/context/notebookVariableContext.js");


const SearchBar = () => {
    const { variables, searchTerm, setSearchTerm } = (0,_context_notebookVariableContext__WEBPACK_IMPORTED_MODULE_1__.useVariableContext)();
    const handleChange = (e) => {
        setSearchTerm(e.target.value);
    };
    return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement((react__WEBPACK_IMPORTED_MODULE_0___default().Fragment), null, variables.length !== 0 ? (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: "mljar-variable-search-bar-container" },
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement("input", { type: "text", value: searchTerm, onChange: handleChange, placeholder: "Search Variable...", className: "mljar-variable-inspector-search-bar-input" }))) : (react__WEBPACK_IMPORTED_MODULE_0___default().createElement((react__WEBPACK_IMPORTED_MODULE_0___default().Fragment), null))));
};


/***/ }),

/***/ "./lib/components/variableInspectorPanel.js":
/*!**************************************************!*\
  !*** ./lib/components/variableInspectorPanel.js ***!
  \**************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   createEmptyVariableInspectorPanel: () => (/* binding */ createEmptyVariableInspectorPanel)
/* harmony export */ });
/* harmony import */ var _variablePanelWidget__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./variablePanelWidget */ "./lib/components/variablePanelWidget.js");
/* harmony import */ var _icons_panelIcon__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../icons/panelIcon */ "./lib/icons/panelIcon.js");


function createEmptyVariableInspectorPanel(labShell, variableName, variableType, variableShape, notebookPanel) {
    const panel = new _variablePanelWidget__WEBPACK_IMPORTED_MODULE_0__.VariablePanelWidget({
        variableName,
        variableType,
        variableShape,
        notebookPanel
    });
    panel.id = `${variableType}-${variableName}`;
    panel.title.label = `${variableType} ${variableName}`;
    panel.title.closable = true;
    panel.title.icon = _icons_panelIcon__WEBPACK_IMPORTED_MODULE_1__.panelIcon;
    const existingPanel = Array.from(labShell.widgets('main')).find(widget => widget.id === panel.id);
    if (existingPanel) {
        labShell.add(panel, 'main', { mode: 'tab-after', ref: existingPanel.id });
    }
    else {
        labShell.add(panel, 'main', { mode: 'split-right' });
    }
    labShell.activateById(panel.id);
}


/***/ }),

/***/ "./lib/components/variableInspectorSidebar.js":
/*!****************************************************!*\
  !*** ./lib/components/variableInspectorSidebar.js ***!
  \****************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   VariableInspectorSidebarWidget: () => (/* binding */ VariableInspectorSidebarWidget),
/* harmony export */   createVariableInspectorSidebar: () => (/* binding */ createVariableInspectorSidebar)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _icons_pluginIcon__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../icons/pluginIcon */ "./lib/icons/pluginIcon.js");
/* harmony import */ var _context_notebookPanelContext__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../context/notebookPanelContext */ "./lib/context/notebookPanelContext.js");
/* harmony import */ var _context_notebookKernelContext__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../context/notebookKernelContext */ "./lib/context/notebookKernelContext.js");
/* harmony import */ var _context_notebookVariableContext__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ../context/notebookVariableContext */ "./lib/context/notebookVariableContext.js");
/* harmony import */ var _variableListComponent__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ./variableListComponent */ "./lib/components/variableListComponent.js");
/* harmony import */ var _context_pluginVisibilityContext__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../context/pluginVisibilityContext */ "./lib/context/pluginVisibilityContext.js");
/* harmony import */ var _context_codeExecutionContext__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ../context/codeExecutionContext */ "./lib/context/codeExecutionContext.js");
// src/components/variableInspectorSidebarWidget.tsx









class VariableInspectorSidebarWidget extends _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__.ReactWidget {
    constructor(notebookWatcher, commands, labShell, settingRegistry, stateDB) {
        super();
        this.isOpen = false;
        this.settingRegistry = null;
        this.notebookWatcher = notebookWatcher;
        this.commands = commands;
        this.id = 'mljar-variable-inspector::mljar-left-sidebar';
        this.title.icon = _icons_pluginIcon__WEBPACK_IMPORTED_MODULE_2__.pluginIcon;
        this.title.caption = 'Variable Inspector';
        this.addClass('mljar-variable-inspector-sidebar-widget');
        this.labShell = labShell;
        this.settingRegistry = settingRegistry;
        this._stateDB = stateDB;
    }
    onAfterShow(msg) {
        super.onAfterShow(msg);
        this.isOpen = true;
        this.update();
    }
    onAfterHide(msg) {
        super.onAfterHide(msg);
        this.isOpen = false;
        this.update();
    }
    render() {
        const contextValue = {
            isPluginOpen: this.isOpen,
            setPluginOpen: open => {
                this.isOpen = open;
                this.update();
            }
        };
        return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: "mljar-variable-inspector-sidebar-container" },
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_context_pluginVisibilityContext__WEBPACK_IMPORTED_MODULE_3__.PluginVisibilityContext.Provider, { value: contextValue },
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_context_notebookPanelContext__WEBPACK_IMPORTED_MODULE_4__.NotebookPanelContextProvider, { notebookWatcher: this.notebookWatcher },
                    react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_context_notebookKernelContext__WEBPACK_IMPORTED_MODULE_5__.NotebookKernelContextProvider, { notebookWatcher: this.notebookWatcher },
                        react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_context_notebookVariableContext__WEBPACK_IMPORTED_MODULE_6__.VariableContextProvider, { stateDB: this._stateDB },
                            react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_context_codeExecutionContext__WEBPACK_IMPORTED_MODULE_7__.CodeExecutionContextProvider, { settingRegistry: this.settingRegistry },
                                react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_variableListComponent__WEBPACK_IMPORTED_MODULE_8__.VariableListComponent, { commands: this.commands, labShell: this.labShell, settingRegistry: this.settingRegistry }))))))));
    }
}
function createVariableInspectorSidebar(notebookWatcher, commands, labShell, settingRegistry, stateDB) {
    return new VariableInspectorSidebarWidget(notebookWatcher, commands, labShell, settingRegistry, stateDB);
}


/***/ }),

/***/ "./lib/components/variableItem.js":
/*!****************************************!*\
  !*** ./lib/components/variableItem.js ***!
  \****************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   VariableItem: () => (/* binding */ VariableItem)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _icons_detailIcon__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../icons/detailIcon */ "./lib/icons/detailIcon.js");
/* harmony import */ var _utils_executeGetMatrix__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../utils/executeGetMatrix */ "./lib/utils/executeGetMatrix.js");
/* harmony import */ var _context_notebookPanelContext__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../context/notebookPanelContext */ "./lib/context/notebookPanelContext.js");
/* harmony import */ var _utils_allowedTypes__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../utils/allowedTypes */ "./lib/utils/allowedTypes.js");
/* harmony import */ var _components_variableInspectorPanel__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../components/variableInspectorPanel */ "./lib/components/variableInspectorPanel.js");






const VariableItem = ({ vrb, commands, labShell, showType, showShape, showSize }) => {
    const notebookPanel = (0,_context_notebookPanelContext__WEBPACK_IMPORTED_MODULE_1__.useNotebookPanelContext)();
    const [loading, setLoading] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)(false);
    const handleButtonClick = async (variableName, variableType, variableShape) => {
        if (notebookPanel) {
            try {
                const result = await (0,_utils_executeGetMatrix__WEBPACK_IMPORTED_MODULE_2__.executeMatrixContent)(variableName, 0, 100, 0, 100, notebookPanel);
                const variableData = result.content;
                let isOpen = false;
                for (const widget of labShell.widgets('main')) {
                    if (widget.id === `${variableType}-${variableName}`) {
                        isOpen = true;
                    }
                }
                if (variableData && !isOpen) {
                    setLoading(true);
                    (0,_components_variableInspectorPanel__WEBPACK_IMPORTED_MODULE_3__.createEmptyVariableInspectorPanel)(labShell, variableName, variableType, variableShape, notebookPanel);
                }
            }
            catch (err) {
                console.error('unknown error', err);
            }
            finally {
                setLoading(false);
            }
        }
    };
    return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("li", { className: `mljar-variable-inspector-item ${_utils_allowedTypes__WEBPACK_IMPORTED_MODULE_4__.allowedTypes.includes(vrb.type) && vrb.dimension <= 2 && vrb.type !== 'list' && vrb.dimension !== 1 ? '' : 'small-value'}` },
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement("span", { className: "mljar-variable-inspector-variable-name" }, vrb.name),
        showType && react__WEBPACK_IMPORTED_MODULE_0___default().createElement("span", { className: "mljar-variable-type" }, vrb.type),
        showShape && (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("span", { className: "mljar-variable-shape" }, vrb.shape !== 'None' ? vrb.shape : '')),
        showSize && (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("span", { className: "mljar-variable-inspector-variable-size" }, vrb.size)),
        _utils_allowedTypes__WEBPACK_IMPORTED_MODULE_4__.allowedTypes.includes(vrb.type) && vrb.dimension <= 2 ? (vrb.dimension === 1 && vrb.type === 'list' ? (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("button", { className: "mljar-variable-inspector-variable-preview", title: vrb.value, onClick: () => handleButtonClick(vrb.name, vrb.type, vrb.shape) }, vrb.value)) : (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("button", { className: "mljar-variable-inspector-show-variable-button", onClick: () => handleButtonClick(vrb.name, vrb.type, vrb.shape), "aria-label": `Show details for ${vrb.name}`, title: "Show value" }, loading ? (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: "mljar-variable-spinner-big" })) : (react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_icons_detailIcon__WEBPACK_IMPORTED_MODULE_5__.detailIcon.react, { className: "mljar-variable-detail-button-icon" }))))) : vrb.type === 'dict' ? (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("span", { className: "mljar-variable-inspector-variable-value", title: vrb.value }, vrb.value)) : (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("span", { className: "mljar-variable-inspector-variable-value", title: vrb.value }, vrb.value))));
};


/***/ }),

/***/ "./lib/components/variableList.js":
/*!****************************************!*\
  !*** ./lib/components/variableList.js ***!
  \****************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   VariableList: () => (/* binding */ VariableList)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _context_notebookVariableContext__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../context/notebookVariableContext */ "./lib/context/notebookVariableContext.js");
/* harmony import */ var _variableItem__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./variableItem */ "./lib/components/variableItem.js");
/* harmony import */ var _index__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../index */ "./lib/index.js");




const VariableList = ({ commands, labShell, settingRegistry }) => {
    const { variables, searchTerm, loading } = (0,_context_notebookVariableContext__WEBPACK_IMPORTED_MODULE_1__.useVariableContext)();
    const filteredVariables = variables.filter(variable => variable.name.toLowerCase().includes(searchTerm.toLowerCase()));
    const [showType, setShowType] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)(false);
    const [showShape, setShowShape] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)(false);
    const [showSize, setShowSize] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)(false);
    const loadPropertiesValues = () => {
        if (settingRegistry) {
            settingRegistry
                .load(_index__WEBPACK_IMPORTED_MODULE_2__.VARIABLE_INSPECTOR_ID)
                .then(settings => {
                const updateSettings = () => {
                    const loadShowType = settings.get(_index__WEBPACK_IMPORTED_MODULE_2__.showTypeProperty)
                        .composite;
                    setShowType(loadShowType);
                    const loadShowShape = settings.get(_index__WEBPACK_IMPORTED_MODULE_2__.showShapeProperty)
                        .composite;
                    setShowShape(loadShowShape);
                    const loadShowSize = settings.get(_index__WEBPACK_IMPORTED_MODULE_2__.showSizeProperty)
                        .composite;
                    setShowSize(loadShowSize);
                };
                updateSettings();
                settings.changed.connect(updateSettings);
            })
                .catch(reason => {
                console.error('Failed to load settings for Variable Inspector', reason);
            });
        }
    };
    (0,react__WEBPACK_IMPORTED_MODULE_0__.useEffect)(() => {
        loadPropertiesValues();
    }, []);
    return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: "mljar-variable-inspector-list-container" }, loading ? (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: "mljar-variable-inspector-message" }, "Loading variables...")) : variables.length === 0 ? (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: "mljar-variable-inspector-message" }, "Sorry, no variables available.")) : (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("ul", { className: "mljar-variable-inspector-list" },
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement("li", { className: "mljar-variable-inspector-header-list" },
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement("span", null, "Name"),
            showType && react__WEBPACK_IMPORTED_MODULE_0___default().createElement("span", null, "Type"),
            showShape && react__WEBPACK_IMPORTED_MODULE_0___default().createElement("span", null, "Shape"),
            showSize && react__WEBPACK_IMPORTED_MODULE_0___default().createElement("span", null, "Size"),
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement("span", null, "Value")),
        filteredVariables.map((variable, index) => (react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_variableItem__WEBPACK_IMPORTED_MODULE_3__.VariableItem, { key: index, vrb: {
                name: variable.name,
                type: variable.type,
                shape: variable.shape,
                dimension: variable.dimension,
                size: variable.size,
                value: variable.value
            }, commands: commands, labShell: labShell, showType: showType, showShape: showShape, showSize: showSize })))))));
};


/***/ }),

/***/ "./lib/components/variableListComponent.js":
/*!*************************************************!*\
  !*** ./lib/components/variableListComponent.js ***!
  \*************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   VariableListComponent: () => (/* binding */ VariableListComponent)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _variableList__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./variableList */ "./lib/components/variableList.js");
/* harmony import */ var _searchBar__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./searchBar */ "./lib/components/searchBar.js");
/* harmony import */ var _variableRefreshButton__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./variableRefreshButton */ "./lib/components/variableRefreshButton.js");
/* harmony import */ var _variableSettingsButton__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./variableSettingsButton */ "./lib/components/variableSettingsButton.js");





const VariableListComponent = ({ commands, labShell, settingRegistry }) => {
    return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: "mljar-variable-inspector-container" },
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: "mljar-variable-header-container" },
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement("h3", { className: "mljar-variable-header" }, "Variable Inspector"),
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_variableRefreshButton__WEBPACK_IMPORTED_MODULE_1__.RefreshButton, { settingRegistry: settingRegistry }),
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_variableSettingsButton__WEBPACK_IMPORTED_MODULE_2__.SettingsButton, { settingRegistry: settingRegistry })),
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", null,
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_searchBar__WEBPACK_IMPORTED_MODULE_3__.SearchBar, null),
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_variableList__WEBPACK_IMPORTED_MODULE_4__.VariableList, { commands: commands, labShell: labShell, settingRegistry: settingRegistry }))));
};


/***/ }),

/***/ "./lib/components/variablePanel.js":
/*!*****************************************!*\
  !*** ./lib/components/variablePanel.js ***!
  \*****************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   VariablePanel: () => (/* binding */ VariablePanel)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var react_virtualized__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! react-virtualized */ "webpack/sharing/consume/default/react-virtualized/react-virtualized");
/* harmony import */ var react_virtualized__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(react_virtualized__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var react_virtualized_styles_css__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! react-virtualized/styles.css */ "./node_modules/react-virtualized/styles.css");
/* harmony import */ var _utils_allowedTypes__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ../utils/allowedTypes */ "./lib/utils/allowedTypes.js");
/* harmony import */ var _utils_executeGetMatrix__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ../utils/executeGetMatrix */ "./lib/utils/executeGetMatrix.js");
/* harmony import */ var _context_variableRefershContext__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../context/variableRefershContext */ "./lib/context/variableRefershContext.js");
/* harmony import */ var _utils_kernelOperationNotifier__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../utils/kernelOperationNotifier */ "./lib/utils/kernelOperationNotifier.js");
/* harmony import */ var _context_themeContext__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../context/themeContext */ "./lib/context/themeContext.js");
/* harmony import */ var _utils_utils__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ../utils/utils */ "./lib/utils/utils.js");
/* harmony import */ var _paginationControls__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! ./paginationControls */ "./lib/components/paginationControls.js");










const AutoSizer = react_virtualized__WEBPACK_IMPORTED_MODULE_1__.AutoSizer;
const MultiGrid = react_virtualized__WEBPACK_IMPORTED_MODULE_1__.MultiGrid;
const VariablePanel = ({ variableName, initVariableType, initVariableShape, notebookPanel }) => {
    var _a;
    const [variableShape, setVariableShape] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)(initVariableShape);
    const [variableType, setVariableType] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)(initVariableType);
    const { isDark } = (0,_context_themeContext__WEBPACK_IMPORTED_MODULE_3__.useThemeContext)();
    const maxRowsRange = 100;
    const maxColsRange = 50;
    const [matrixData, setMatrixData] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)([]);
    const { refreshCount } = (0,_context_variableRefershContext__WEBPACK_IMPORTED_MODULE_4__.useVariableRefeshContext)();
    const [currentRow, setCurrentRow] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)(0);
    const [currentColumn, setCurrentColumn] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)(0);
    const [returnedSize, setReturnedSize] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)([]);
    const [rowInput, setRowInput] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)(currentRow.toString());
    const [columnInput, setColumnInput] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)(currentColumn.toString());
    const [rowsCount, setRowsCount] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)(parseDimensions(variableShape)[0]);
    const [colsCount, setColsCount] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)(parseDimensions(variableShape)[1]);
    const [autoSizerKey, setAutoSizerKey] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)(0);
    const containerRef = (0,react__WEBPACK_IMPORTED_MODULE_0__.useRef)(null);
    const [cellRowInput, setCellRowInput] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)('');
    const [cellColumnInput, setCellColumnInput] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)('');
    const [gotoCell, setGotoCell] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)(null);
    const [highlightCell, setHighlightCell] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)(null);
    const fetchMatrixData = (0,react__WEBPACK_IMPORTED_MODULE_0__.useCallback)(async () => {
        try {
            if (!notebookPanel) {
                return;
            }
            const result = await (0,_utils_kernelOperationNotifier__WEBPACK_IMPORTED_MODULE_5__.withIgnoredPanelKernelUpdates)(() => (0,_utils_executeGetMatrix__WEBPACK_IMPORTED_MODULE_6__.executeMatrixContent)(variableName, currentColumn, currentColumn + maxColsRange > colsCount
                ? colsCount
                : currentColumn + maxColsRange, currentRow, currentRow + maxRowsRange > rowsCount
                ? rowsCount
                : currentRow + maxRowsRange, notebookPanel));
            setVariableShape(result.variableShape);
            setVariableType(result.variableType);
            setReturnedSize(result.returnedSize);
            setMatrixData(result.content);
        }
        catch (error) {
            console.error('Error fetching matrix content:', error);
        }
    }, [
        notebookPanel,
        variableName,
        currentColumn,
        currentRow,
        maxColsRange,
        maxRowsRange,
        _utils_kernelOperationNotifier__WEBPACK_IMPORTED_MODULE_5__.withIgnoredPanelKernelUpdates,
        _utils_executeGetMatrix__WEBPACK_IMPORTED_MODULE_6__.executeMatrixContent,
        setVariableShape,
        setVariableType,
        setReturnedSize,
        setMatrixData,
        variableType,
        returnedSize
    ]);
    (0,react__WEBPACK_IMPORTED_MODULE_0__.useEffect)(() => {
        setRowInput(currentRow.toString());
    }, [currentRow]);
    (0,react__WEBPACK_IMPORTED_MODULE_0__.useEffect)(() => {
        setColumnInput(currentColumn.toString());
    }, [currentColumn]);
    (0,react__WEBPACK_IMPORTED_MODULE_0__.useEffect)(() => {
        fetchMatrixData();
        const [rows, cols] = parseDimensions(variableShape);
        setRowsCount(rows);
        setColsCount(cols);
    }, [refreshCount]);
    (0,react__WEBPACK_IMPORTED_MODULE_0__.useEffect)(() => {
        fetchMatrixData();
    }, [currentRow, currentColumn]);
    (0,react__WEBPACK_IMPORTED_MODULE_0__.useEffect)(() => {
        if (containerRef.current) {
            const resizeObserver = new ResizeObserver(entries => {
                for (const entry of entries) {
                    void entry;
                    setAutoSizerKey(prev => prev + 1);
                }
            });
            resizeObserver.observe(containerRef.current);
            return () => {
                resizeObserver.disconnect();
            };
        }
    }, []);
    const handlePrevRowPage = (value) => {
        if (value === 'previous') {
            if (currentRow > maxRowsRange - 1) {
                setCurrentRow(currentRow - maxRowsRange);
            }
            else {
                setCurrentRow(0);
            }
        }
        if (value === 'first') {
            setCurrentRow(0);
        }
    };
    const handleNextRowPage = (value) => {
        if (rowsCount > maxRowsRange) {
            if (value === 'next') {
                if (currentRow + 2 * maxRowsRange < rowsCount) {
                    setCurrentRow(currentRow + maxRowsRange);
                }
                else {
                    setCurrentRow(rowsCount - maxRowsRange);
                }
            }
            if (value === 'last') {
                setCurrentRow(rowsCount - maxRowsRange);
            }
        }
        else {
            setCurrentRow(0);
        }
    };
    const handlePrevColumnPage = (value) => {
        if (value === 'previous') {
            if (currentColumn > maxColsRange - 1) {
                setCurrentColumn(currentColumn - maxColsRange);
            }
            else {
                setCurrentColumn(0);
            }
        }
        if (value === 'first') {
            setCurrentColumn(0);
        }
    };
    const handleNextColumnPage = (value) => {
        if (colsCount > maxColsRange) {
            if (value === 'next') {
                if (currentColumn + 2 * maxColsRange < colsCount) {
                    setCurrentColumn(currentColumn + maxColsRange);
                }
                else {
                    setCurrentColumn(colsCount - maxColsRange);
                }
            }
            if (value === 'last') {
                setCurrentColumn(colsCount - maxColsRange);
            }
        }
        else {
            setCurrentColumn(0);
        }
    };
    function parseDimensions(input) {
        const regex2D = /^(-?\d+)\s*x\s*(-?\d+)$/;
        const match2D = input.match(regex2D);
        if (match2D) {
            const a = parseInt(match2D[1], 10);
            const b = parseInt(match2D[2], 10);
            return [a, b];
        }
        const regex1D = /^-?\d+$/;
        if (input.match(regex1D)) {
            const n = parseInt(input, 10);
            return [n, 1];
        }
        throw new Error('Wrong format');
    }
    const { data, fixedRowCount, fixedColumnCount } = (0,_utils_utils__WEBPACK_IMPORTED_MODULE_7__.transformMatrixData)(matrixData, variableType, currentRow, currentColumn);
    const rowCount = data.length;
    const colCount = ((_a = data[0]) === null || _a === void 0 ? void 0 : _a.length) || 0;
    const columnWidths = [];
    for (let col = 0; col < colCount; col++) {
        let maxLength = 0;
        for (let row = 0; row < rowCount; row++) {
            const cell = data[row][col];
            const cellStr = cell !== null ? cell.toString() : '';
            if (cellStr.length > maxLength) {
                maxLength = cellStr.length;
            }
        }
        columnWidths[col] = maxLength * 7 + 16;
    }
    const cellRenderer = ({ columnIndex, key, rowIndex, style }) => {
        const cellData = data[rowIndex][columnIndex];
        let cellStyle = {
            ...style,
            boxSizing: 'border-box',
            border: `1px solid ${isDark ? '#444' : '#ddd'}`,
            fontSize: '0.75rem',
            padding: '2px',
            color: isDark ? '#ddd' : '#000',
            background: isDark
                ? rowIndex % 2 === 0
                    ? '#333'
                    : '#222'
                : rowIndex % 2 === 0
                    ? '#fafafa'
                    : '#fff'
        };
        if (highlightCell &&
            rowIndex === highlightCell.row &&
            columnIndex === highlightCell.column) {
            cellStyle = {
                ...cellStyle,
                border: '2px solid #0099cc'
            };
        }
        if (rowIndex === 0 || columnIndex === 0) {
            cellStyle = {
                ...cellStyle,
                background: isDark ? '#555' : '#e0e0e0',
                fontWeight: 'bold',
                textAlign: 'center'
            };
        }
        return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { key: key, style: cellStyle }, typeof cellData === 'boolean'
            ? cellData
                ? 'True'
                : 'False'
            : cellData));
    };
    const handleGotoCell = () => {
        const targetGlobalRow = parseInt(cellRowInput, 10);
        const targetGlobalCol = parseInt(cellColumnInput, 10);
        if (!isNaN(targetGlobalRow) &&
            targetGlobalRow >= 0 &&
            !isNaN(targetGlobalCol) &&
            targetGlobalCol >= 0) {
            const newRowPage = Math.floor(targetGlobalRow / maxRowsRange) + 1;
            const newColPage = Math.floor(targetGlobalCol / maxColsRange) + 1;
            setRowInput(newRowPage.toString());
            setColumnInput(newColPage.toString());
            const localRow = targetGlobalRow - (newRowPage - 1) * maxRowsRange;
            const localCol = targetGlobalCol - (newColPage - 1) * maxColsRange;
            const gridRow = fixedRowCount + localRow;
            const gridCol = fixedColumnCount + localCol;
            setCurrentRow(newRowPage);
            setCurrentColumn(newColPage);
            setTimeout(() => {
                setGotoCell({ row: gridRow, column: gridCol });
                setHighlightCell({ row: gridRow, column: gridCol });
                setTimeout(() => {
                    setHighlightCell(null);
                }, 2000);
            }, 500);
        }
    };
    if (!_utils_allowedTypes__WEBPACK_IMPORTED_MODULE_8__.allowedTypes.includes(variableType)) {
        return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { style: {
                padding: '10px',
                fontSize: '16px',
                height: '100%',
                background: isDark ? '#222' : '#fff',
                color: isDark ? '#ddd' : '#000'
            } },
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement("p", null,
                "Wrong variable type: ",
                variableType)));
    }
    return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { ref: containerRef, className: "mljar-variable-inspector-pagination-container", style: {
            height: '100%',
            background: isDark ? '#222' : '#fff',
            color: isDark ? '#ddd' : '#000'
        } },
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { style: { height: '90%' } },
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement(AutoSizer, { key: autoSizerKey }, ({ width, height }) => (react__WEBPACK_IMPORTED_MODULE_0___default().createElement(MultiGrid, { fixedRowCount: fixedRowCount, fixedColumnCount: fixedColumnCount, cellRenderer: cellRenderer, columnCount: colCount, columnWidth: ({ index }) => columnWidths[index], rowHeight: 20, height: height, rowCount: rowCount, width: width, scrollToRow: gotoCell ? gotoCell.row : undefined, scrollToColumn: gotoCell ? gotoCell.column : undefined, styleTopLeftGrid: { background: isDark ? '#555' : '#e0e0e0' }, styleTopRightGrid: { background: isDark ? '#555' : '#e0e0e0' }, styleBottomLeftGrid: { background: isDark ? '#222' : '#fff' }, styleBottomRightGrid: { background: isDark ? '#222' : '#fff' } })))),
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", null,
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_paginationControls__WEBPACK_IMPORTED_MODULE_9__.PaginationControls, { rowsCount: rowsCount, colsCount: colsCount, rowInput: rowInput, setRowInput: setRowInput, currentRow: currentRow, setCurrentRow: setCurrentRow, columnInput: columnInput, setColumnInput: setColumnInput, currentColumn: currentColumn, setCurrentColumn: setCurrentColumn, cellRowInput: cellRowInput, setCellRowInput: setCellRowInput, cellColumnInput: cellColumnInput, setCellColumnInput: setCellColumnInput, handleGotoCell: handleGotoCell, handlePrevRowPage: handlePrevRowPage, handleNextRowPage: handleNextRowPage, handlePrevColumnPage: handlePrevColumnPage, handleNextColumnPage: handleNextColumnPage }))));
};


/***/ }),

/***/ "./lib/components/variablePanelWidget.js":
/*!***********************************************!*\
  !*** ./lib/components/variablePanelWidget.js ***!
  \***********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   VariablePanelWidget: () => (/* binding */ VariablePanelWidget)
/* harmony export */ });
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _variablePanel__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./variablePanel */ "./lib/components/variablePanel.js");
/* harmony import */ var _context_variableRefershContext__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../context/variableRefershContext */ "./lib/context/variableRefershContext.js");
/* harmony import */ var _context_themeContext__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../context/themeContext */ "./lib/context/themeContext.js");





class VariablePanelWidget extends _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.ReactWidget {
    constructor(props) {
        super();
        this.props = props;
        this.update();
    }
    render() {
        return (react__WEBPACK_IMPORTED_MODULE_1___default().createElement("div", { style: { height: '100%', width: '100%' } },
            react__WEBPACK_IMPORTED_MODULE_1___default().createElement(_context_variableRefershContext__WEBPACK_IMPORTED_MODULE_2__.VariableRefreshContextProvider, { notebookPanel: this.props.notebookPanel },
                react__WEBPACK_IMPORTED_MODULE_1___default().createElement(_context_themeContext__WEBPACK_IMPORTED_MODULE_3__.ThemeContextProvider, null,
                    react__WEBPACK_IMPORTED_MODULE_1___default().createElement(_variablePanel__WEBPACK_IMPORTED_MODULE_4__.VariablePanel, { variableName: this.props.variableName, initVariableType: this.props.variableType, initVariableShape: this.props.variableShape, notebookPanel: this.props.notebookPanel })))));
    }
}


/***/ }),

/***/ "./lib/components/variableRefreshButton.js":
/*!*************************************************!*\
  !*** ./lib/components/variableRefreshButton.js ***!
  \*************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   RefreshButton: () => (/* binding */ RefreshButton)
/* harmony export */ });
/* harmony import */ var _icons_refreshIcon__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../icons/refreshIcon */ "./lib/icons/refreshIcon.js");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _context_notebookVariableContext__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../context/notebookVariableContext */ "./lib/context/notebookVariableContext.js");
/* harmony import */ var _index__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../index */ "./lib/index.js");




const RefreshButton = ({ settingRegistry }) => {
    const { refreshVariables, loading } = (0,_context_notebookVariableContext__WEBPACK_IMPORTED_MODULE_1__.useVariableContext)();
    const [autoRefresh, setAutoRefresh] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)(true);
    const loadAutoRefresh = () => {
        if (settingRegistry) {
            settingRegistry
                .load(_index__WEBPACK_IMPORTED_MODULE_2__.VARIABLE_INSPECTOR_ID)
                .then(settings => {
                const updateSettings = () => {
                    const loadAutoRefresh = settings.get(_index__WEBPACK_IMPORTED_MODULE_2__.autoRefreshProperty)
                        .composite;
                    setAutoRefresh(loadAutoRefresh);
                };
                updateSettings();
                settings.changed.connect(updateSettings);
            })
                .catch(reason => {
                console.error('Failed to load settings for Variable Inspector', reason);
            });
        }
    };
    (0,react__WEBPACK_IMPORTED_MODULE_0__.useEffect)(() => {
        loadAutoRefresh();
    }, []);
    return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("button", { className: `mljar-variable-inspector-refresh-button ${autoRefresh ? `` : `manually-refresh`}`, onClick: refreshVariables, disabled: loading, title: "Refresh Variables" },
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_icons_refreshIcon__WEBPACK_IMPORTED_MODULE_3__.refreshIcon.react, { className: "mljar-variable-inspector-refresh-icon" })));
};


/***/ }),

/***/ "./lib/components/variableSettingsButton.js":
/*!**************************************************!*\
  !*** ./lib/components/variableSettingsButton.js ***!
  \**************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   SettingsButton: () => (/* binding */ SettingsButton)
/* harmony export */ });
/* harmony import */ var _icons_settingsIcon__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../icons/settingsIcon */ "./lib/icons/settingsIcon.js");
/* harmony import */ var _icons_checkIcon__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../icons/checkIcon */ "./lib/icons/checkIcon.js");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _index__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../index */ "./lib/index.js");




const SettingsButton = ({ settingRegistry }) => {
    const [isOpen, setIsOpen] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)(false);
    const [autoRefresh, setAutoRefresh] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)(true);
    const [showType, setShowType] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)(false);
    const [showShape, setShowShape] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)(false);
    const [showSize, setShowSize] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)(false);
    const showSettings = () => {
        setIsOpen(!isOpen);
    };
    const savePropertyValue = (propertyName, newValue) => {
        if (settingRegistry) {
            settingRegistry
                .load(_index__WEBPACK_IMPORTED_MODULE_1__.VARIABLE_INSPECTOR_ID)
                .then(settings => {
                settings.set(propertyName, newValue);
            })
                .catch(reason => {
                console.error(`Faild to save ${propertyName}: `, reason);
            });
        }
    };
    const loadPropertiesValues = () => {
        if (settingRegistry) {
            settingRegistry
                .load(_index__WEBPACK_IMPORTED_MODULE_1__.VARIABLE_INSPECTOR_ID)
                .then(settings => {
                const updateSettings = () => {
                    const loadAutoRefresh = settings.get(_index__WEBPACK_IMPORTED_MODULE_1__.autoRefreshProperty)
                        .composite;
                    setAutoRefresh(loadAutoRefresh);
                    const loadShowType = settings.get(_index__WEBPACK_IMPORTED_MODULE_1__.showTypeProperty)
                        .composite;
                    setShowType(loadShowType);
                    const loadShowShape = settings.get(_index__WEBPACK_IMPORTED_MODULE_1__.showShapeProperty)
                        .composite;
                    setShowShape(loadShowShape);
                    const loadShowSize = settings.get(_index__WEBPACK_IMPORTED_MODULE_1__.showSizeProperty)
                        .composite;
                    setShowSize(loadShowSize);
                };
                updateSettings();
                settings.changed.connect(updateSettings);
            })
                .catch(reason => {
                console.error('Failed to load settings for Variable Inspector', reason);
            });
        }
    };
    (0,react__WEBPACK_IMPORTED_MODULE_0__.useEffect)(() => {
        loadPropertiesValues();
    }, []);
    return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: "mljar-variable-inspector-settings-container" },
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement("button", { className: `mljar-variable-inspector-settings-button ${isOpen ? 'active' : ''}`, onClick: showSettings, title: "Settings" },
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_icons_settingsIcon__WEBPACK_IMPORTED_MODULE_2__.settingsIcon.react, { className: "mljar-variable-inspector-settings-icon" })),
        isOpen && (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: "mljar-variable-inspector-settings-menu" },
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement("ul", { className: "mljar-variable-inspector-settings-menu-list" },
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement("button", { className: "mljar-variable-inspector-settings-menu-item first", onClick: () => {
                        if (!autoRefresh)
                            savePropertyValue(_index__WEBPACK_IMPORTED_MODULE_1__.autoRefreshProperty, true);
                    } },
                    "Automatically refresh",
                    autoRefresh && (react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_icons_checkIcon__WEBPACK_IMPORTED_MODULE_3__.checkIcon.react, { className: "mljar-variable-inspector-settings-icon" }))),
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement("button", { className: "mljar-variable-inspector-settings-menu-item", onClick: () => {
                        if (autoRefresh)
                            savePropertyValue(_index__WEBPACK_IMPORTED_MODULE_1__.autoRefreshProperty, false);
                    } },
                    "Manually refresh",
                    !autoRefresh && (react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_icons_checkIcon__WEBPACK_IMPORTED_MODULE_3__.checkIcon.react, { className: "mljar-variable-inspector-settings-icon" }))),
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement("hr", null),
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement("button", { className: "mljar-variable-inspector-settings-menu-item", onClick: () => savePropertyValue(_index__WEBPACK_IMPORTED_MODULE_1__.showTypeProperty, !showType) },
                    "Show type",
                    showType && (react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_icons_checkIcon__WEBPACK_IMPORTED_MODULE_3__.checkIcon.react, { className: "mljar-variable-inspector-settings-icon" }))),
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement("button", { className: "mljar-variable-inspector-settings-menu-item", onClick: () => savePropertyValue(_index__WEBPACK_IMPORTED_MODULE_1__.showShapeProperty, !showShape) },
                    "Show shape",
                    showShape && (react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_icons_checkIcon__WEBPACK_IMPORTED_MODULE_3__.checkIcon.react, { className: "mljar-variable-inspector-settings-icon" }))),
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement("button", { className: "mljar-variable-inspector-settings-menu-item last", onClick: () => savePropertyValue(_index__WEBPACK_IMPORTED_MODULE_1__.showSizeProperty, !showSize) },
                    "Show size",
                    showSize && (react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_icons_checkIcon__WEBPACK_IMPORTED_MODULE_3__.checkIcon.react, { className: "mljar-variable-inspector-settings-icon" }))))))));
};


/***/ }),

/***/ "./lib/context/codeExecutionContext.js":
/*!*********************************************!*\
  !*** ./lib/context/codeExecutionContext.js ***!
  \*********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   CodeExecutionContextProvider: () => (/* binding */ CodeExecutionContextProvider),
/* harmony export */   useCodeExecutionContext: () => (/* binding */ useCodeExecutionContext)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _notebookPanelContext__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./notebookPanelContext */ "./lib/context/notebookPanelContext.js");
/* harmony import */ var _notebookKernelContext__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./notebookKernelContext */ "./lib/context/notebookKernelContext.js");
/* harmony import */ var _notebookVariableContext__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./notebookVariableContext */ "./lib/context/notebookVariableContext.js");
/* harmony import */ var _index__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../index */ "./lib/index.js");
/* harmony import */ var _python_code_getVariables__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../python_code/getVariables */ "./lib/python_code/getVariables.js");






const CodeExecutionContext = (0,react__WEBPACK_IMPORTED_MODULE_0__.createContext)(undefined);
const CodeExecutionContextProvider = ({ children, settingRegistry }) => {
    const notebook = (0,_notebookPanelContext__WEBPACK_IMPORTED_MODULE_1__.useNotebookPanelContext)();
    const kernelReady = (0,_notebookKernelContext__WEBPACK_IMPORTED_MODULE_2__.useNotebookKernelContext)();
    const { refreshVariables } = (0,_notebookVariableContext__WEBPACK_IMPORTED_MODULE_3__.useVariableContext)();
    const getVariableCode = _python_code_getVariables__WEBPACK_IMPORTED_MODULE_4__.variableDict;
    const [autoRefresh, setAutoRefresh] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)(true);
    const loadAutoRefresh = () => {
        if (settingRegistry) {
            settingRegistry
                .load(_index__WEBPACK_IMPORTED_MODULE_5__.VARIABLE_INSPECTOR_ID)
                .then(settings => {
                const updateSettings = () => {
                    const loadAutoRefresh = settings.get(_index__WEBPACK_IMPORTED_MODULE_5__.autoRefreshProperty)
                        .composite;
                    setAutoRefresh(loadAutoRefresh);
                };
                updateSettings();
                settings.changed.connect(updateSettings);
            })
                .catch(reason => {
                console.error('Failed to load settings for Variable Inspector', reason);
            });
        }
    };
    (0,react__WEBPACK_IMPORTED_MODULE_0__.useEffect)(() => {
        loadAutoRefresh();
    }, []);
    (0,react__WEBPACK_IMPORTED_MODULE_0__.useEffect)(() => {
        var _a, _b;
        if (!notebook) {
            return;
        }
        const kernel = (_b = (_a = notebook.sessionContext) === null || _a === void 0 ? void 0 : _a.session) === null || _b === void 0 ? void 0 : _b.kernel;
        if (!kernel) {
            return;
        }
        const handleIOPubMessage = (sender, msg) => {
            if (msg.header.msg_type === 'execute_input') {
                const inputMsg = msg;
                const code = inputMsg.content.code;
                const variableInspectorPrefix = '_jupyterlab_variableinspector';
                const mljarPrefix = '__mljar';
                if (code !== getVariableCode &&
                    !code.includes(variableInspectorPrefix) &&
                    !code.includes(mljarPrefix) &&
                    autoRefresh) {
                    refreshVariables();
                }
            }
        };
        kernel.iopubMessage.connect(handleIOPubMessage);
        return () => {
            kernel.iopubMessage.disconnect(handleIOPubMessage);
        };
    }, [notebook, notebook === null || notebook === void 0 ? void 0 : notebook.sessionContext, kernelReady, autoRefresh]);
    return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement(CodeExecutionContext.Provider, { value: {} }, children));
};
const useCodeExecutionContext = () => {
    const context = (0,react__WEBPACK_IMPORTED_MODULE_0__.useContext)(CodeExecutionContext);
    if (!context) {
        throw new Error('useCodeExecutionContext must be used CodeExecutionContextProvider');
    }
    return context;
};


/***/ }),

/***/ "./lib/context/notebookKernelContext.js":
/*!**********************************************!*\
  !*** ./lib/context/notebookKernelContext.js ***!
  \**********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   NotebookKernelContextProvider: () => (/* binding */ NotebookKernelContextProvider),
/* harmony export */   useNotebookKernelContext: () => (/* binding */ useNotebookKernelContext)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);

const NotebookKernelContext = (0,react__WEBPACK_IMPORTED_MODULE_0__.createContext)(null);
function useNotebookKernelContext() {
    return (0,react__WEBPACK_IMPORTED_MODULE_0__.useContext)(NotebookKernelContext);
}
function NotebookKernelContextProvider({ children, notebookWatcher }) {
    const [kernelInfo, setKernelInfo] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)(notebookWatcher.kernelInfo);
    (0,react__WEBPACK_IMPORTED_MODULE_0__.useEffect)(() => {
        const onKernelChanged = (sender, newKernelInfo) => {
            setKernelInfo(newKernelInfo);
        };
        notebookWatcher.kernelChanged.connect(onKernelChanged);
        setKernelInfo(notebookWatcher.kernelInfo);
        return () => {
            notebookWatcher.kernelChanged.disconnect(onKernelChanged);
        };
    }, [notebookWatcher]);
    return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement(NotebookKernelContext.Provider, { value: kernelInfo }, children));
}


/***/ }),

/***/ "./lib/context/notebookPanelContext.js":
/*!*********************************************!*\
  !*** ./lib/context/notebookPanelContext.js ***!
  \*********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   NotebookPanelContextProvider: () => (/* binding */ NotebookPanelContextProvider),
/* harmony export */   useNotebookPanelContext: () => (/* binding */ useNotebookPanelContext)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);

const NotebookPanelContext = (0,react__WEBPACK_IMPORTED_MODULE_0__.createContext)(null);
function useNotebookPanelContext() {
    return (0,react__WEBPACK_IMPORTED_MODULE_0__.useContext)(NotebookPanelContext);
}
function NotebookPanelContextProvider({ children, notebookWatcher }) {
    const [notebookPanel, setNotebookPanel] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)(notebookWatcher.notebookPanel());
    (0,react__WEBPACK_IMPORTED_MODULE_0__.useEffect)(() => {
        const onNotebookPanelChange = (sender, newNotebookPanel) => {
            setNotebookPanel(newNotebookPanel);
        };
        notebookWatcher.notebookPanelChanged.connect(onNotebookPanelChange);
        setNotebookPanel(notebookWatcher.notebookPanel());
        return () => {
            notebookWatcher.notebookPanelChanged.disconnect(onNotebookPanelChange);
        };
    }, [notebookWatcher]);
    return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement(NotebookPanelContext.Provider, { value: notebookPanel }, children));
}


/***/ }),

/***/ "./lib/context/notebookVariableContext.js":
/*!************************************************!*\
  !*** ./lib/context/notebookVariableContext.js ***!
  \************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   VariableContextProvider: () => (/* binding */ VariableContextProvider),
/* harmony export */   useVariableContext: () => (/* binding */ useVariableContext)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _notebookPanelContext__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./notebookPanelContext */ "./lib/context/notebookPanelContext.js");
/* harmony import */ var _notebookKernelContext__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./notebookKernelContext */ "./lib/context/notebookKernelContext.js");
/* harmony import */ var _utils_kernelOperationNotifier__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../utils/kernelOperationNotifier */ "./lib/utils/kernelOperationNotifier.js");
/* harmony import */ var _python_code_getVariables__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../python_code/getVariables */ "./lib/python_code/getVariables.js");





const VariableContext = (0,react__WEBPACK_IMPORTED_MODULE_0__.createContext)(undefined);
class DebouncedTaskQueue {
    /**
     * @param delay Time in milliseconds to wait before executing the last task.
     */
    constructor(delay = 500) {
        // Holds the timer handle.
        this.timer = null;
        // Holds the most recently added task.
        this.lastTask = null;
        this.delay = delay;
    }
    /**
     * Adds a new task to the queue. Only the last task added within the delay period will be executed.
     * @param task A function representing the task.
     */
    add(task) {
        // Save (or overwrite) the latest task.
        this.lastTask = task;
        // If there’s already a pending timer, clear it.
        if (this.timer) {
            clearTimeout(this.timer);
        }
        // Start (or restart) the timer.
        this.timer = setTimeout(async () => {
            if (this.lastTask) {
                try {
                    // Execute the latest task.
                    await this.lastTask();
                }
                catch (error) {
                    console.error('Task execution failed:', error);
                }
            }
            // After execution, clear the stored task and timer.
            this.lastTask = null;
            this.timer = null;
        }, this.delay);
    }
}
const VariableContextProvider = ({ children, stateDB }) => {
    const notebookPanel = (0,_notebookPanelContext__WEBPACK_IMPORTED_MODULE_1__.useNotebookPanelContext)();
    const kernel = (0,_notebookKernelContext__WEBPACK_IMPORTED_MODULE_2__.useNotebookKernelContext)();
    const [variables, setVariables] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)([]);
    const [loading, setLoading] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)(false);
    const [error, setError] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)(null);
    const [searchTerm, setSearchTerm] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)('');
    const [isRefreshing, setIsRefreshing] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)(false);
    const [refreshCount, setRefreshCount] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)(0);
    const queue = new DebouncedTaskQueue(250);
    const executeCode = (0,react__WEBPACK_IMPORTED_MODULE_0__.useCallback)(async () => {
        await (0,_utils_kernelOperationNotifier__WEBPACK_IMPORTED_MODULE_3__.withIgnoredSidebarKernelUpdates)(async () => {
            var _a, _b, _c;
            //setIsRefreshing(true);
            //setLoading(true);
            setError(null);
            if (!notebookPanel) {
                setVariables([]);
                setLoading(false);
                setIsRefreshing(false);
                return;
            }
            //setVariables([]);
            try {
                const future = (_c = (_b = (_a = notebookPanel.sessionContext) === null || _a === void 0 ? void 0 : _a.session) === null || _b === void 0 ? void 0 : _b.kernel) === null || _c === void 0 ? void 0 : _c.requestExecute({
                    code: _python_code_getVariables__WEBPACK_IMPORTED_MODULE_4__.variableDict,
                    store_history: false
                });
                if (future) {
                    future.onIOPub = (msg) => {
                        const msgType = msg.header.msg_type;
                        if (msgType === 'execute_result' ||
                            msgType === 'display_data' ||
                            msgType === 'update_display_data' ||
                            msgType === 'error') {
                            const content = msg.content;
                            const jsonData = content.data['application/json'];
                            const textData = content.data['text/plain'];
                            if (jsonData) {
                                setLoading(false);
                                setIsRefreshing(false);
                                setRefreshCount(prev => prev + 1);
                            }
                            else if (textData) {
                                try {
                                    const cleanedData = textData.replace(/^['"]|['"]$/g, '');
                                    const doubleQuotedData = cleanedData.replace(/'/g, '"');
                                    const parsedData = JSON.parse(doubleQuotedData);
                                    if (Array.isArray(parsedData)) {
                                        const mappedVariables = parsedData.map((item) => ({
                                            name: item.varName,
                                            type: item.varType,
                                            shape: item.varShape || 'None',
                                            dimension: item.varDimension,
                                            size: item.varSize,
                                            value: item.varSimpleValue
                                        }));
                                        setVariables(mappedVariables);
                                    }
                                    else {
                                        throw new Error('Error during parsing.');
                                    }
                                    setLoading(false);
                                    setIsRefreshing(false);
                                    setRefreshCount(prev => prev + 1);
                                }
                                catch (err) {
                                    setError('Error during export JSON.');
                                    setVariables([]);
                                    setLoading(false);
                                    setIsRefreshing(false);
                                }
                            }
                        }
                    };
                }
            }
            catch (err) {
                setError('Unexpected error.');
                setLoading(false);
                setIsRefreshing(false);
            }
        });
        return;
    }, [notebookPanel, kernel]);
    (0,react__WEBPACK_IMPORTED_MODULE_0__.useEffect)(() => {
        executeCode();
    }, [executeCode]);
    return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement(VariableContext.Provider, { value: {
            variables,
            loading,
            error,
            searchTerm,
            setSearchTerm,
            refreshVariables: () => queue.add(() => executeCode()),
            isRefreshing,
            refreshCount
        } }, children));
};
const useVariableContext = () => {
    const context = (0,react__WEBPACK_IMPORTED_MODULE_0__.useContext)(VariableContext);
    if (context === undefined) {
        throw new Error('useVariableContext must be used within a VariableProvider');
    }
    return context;
};


/***/ }),

/***/ "./lib/context/pluginVisibilityContext.js":
/*!************************************************!*\
  !*** ./lib/context/pluginVisibilityContext.js ***!
  \************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   PluginVisibilityContext: () => (/* binding */ PluginVisibilityContext),
/* harmony export */   PluginVisibilityProvider: () => (/* binding */ PluginVisibilityProvider),
/* harmony export */   usePluginVisibility: () => (/* binding */ usePluginVisibility)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);

const PluginVisibilityContext = (0,react__WEBPACK_IMPORTED_MODULE_0__.createContext)({
    isPluginOpen: false,
    setPluginOpen: () => { }
});
function PluginVisibilityProvider({ children }) {
    const [isPluginOpen, setPluginOpen] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)(false);
    return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement(PluginVisibilityContext.Provider, { value: { isPluginOpen, setPluginOpen } }, children));
}
function usePluginVisibility() {
    return (0,react__WEBPACK_IMPORTED_MODULE_0__.useContext)(PluginVisibilityContext);
}


/***/ }),

/***/ "./lib/context/themeContext.js":
/*!*************************************!*\
  !*** ./lib/context/themeContext.js ***!
  \*************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   ThemeContextProvider: () => (/* binding */ ThemeContextProvider),
/* harmony export */   useThemeContext: () => (/* binding */ useThemeContext)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);

const ThemeContext = (0,react__WEBPACK_IMPORTED_MODULE_0__.createContext)({ isDark: false });
const ThemeContextProvider = ({ children }) => {
    const [isDark, setIsDark] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)(() => {
        const theme = document.body.dataset.jpThemeName;
        return theme ? theme.includes('Dark') : false;
    });
    (0,react__WEBPACK_IMPORTED_MODULE_0__.useEffect)(() => {
        const observer = new MutationObserver(mutations => {
            mutations.forEach(mutation => {
                var _a;
                if (mutation.type === 'attributes' && mutation.attributeName === 'data-jp-theme-name') {
                    const theme = document.body.getAttribute('data-jp-theme-name');
                    setIsDark((_a = theme === null || theme === void 0 ? void 0 : theme.includes('Dark')) !== null && _a !== void 0 ? _a : false);
                }
            });
        });
        observer.observe(document.body, {
            attributes: true,
            attributeFilter: ['data-jp-theme-name']
        });
        return () => {
            observer.disconnect();
        };
    }, []);
    return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement(ThemeContext.Provider, { value: { isDark } }, children));
};
const useThemeContext = () => (0,react__WEBPACK_IMPORTED_MODULE_0__.useContext)(ThemeContext);


/***/ }),

/***/ "./lib/context/variableRefershContext.js":
/*!***********************************************!*\
  !*** ./lib/context/variableRefershContext.js ***!
  \***********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   VariableRefreshContextProvider: () => (/* binding */ VariableRefreshContextProvider),
/* harmony export */   useVariableRefeshContext: () => (/* binding */ useVariableRefeshContext)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _utils_kernelOperationNotifier__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../utils/kernelOperationNotifier */ "./lib/utils/kernelOperationNotifier.js");


const VariableRefreshContext = (0,react__WEBPACK_IMPORTED_MODULE_0__.createContext)({
    refreshCount: 0
});
const VariableRefreshContextProvider = ({ children, notebookPanel }) => {
    const [refreshCount, setRefreshCount] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)(0);
    (0,react__WEBPACK_IMPORTED_MODULE_0__.useEffect)(() => {
        var _a;
        if (!notebookPanel) {
            return;
        }
        const kernel = (_a = notebookPanel.sessionContext.session) === null || _a === void 0 ? void 0 : _a.kernel;
        if (!kernel) {
            return;
        }
        const onSidebarStatusChange = (_sender, inProgress) => {
            if (inProgress === true) {
                setRefreshCount(prev => prev + 1);
            }
        };
        _utils_kernelOperationNotifier__WEBPACK_IMPORTED_MODULE_1__.kernelOperationNotifier.sidebarOperationChanged.connect(onSidebarStatusChange);
        return () => {
            _utils_kernelOperationNotifier__WEBPACK_IMPORTED_MODULE_1__.kernelOperationNotifier.sidebarOperationChanged.disconnect(onSidebarStatusChange);
        };
    }, [notebookPanel]);
    return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement(VariableRefreshContext.Provider, { value: { refreshCount } }, children));
};
const useVariableRefeshContext = () => (0,react__WEBPACK_IMPORTED_MODULE_0__.useContext)(VariableRefreshContext);


/***/ }),

/***/ "./lib/icons/checkIcon.js":
/*!********************************!*\
  !*** ./lib/icons/checkIcon.js ***!
  \********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   checkIcon: () => (/* binding */ checkIcon)
/* harmony export */ });
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__);

const svgStr = `
<svg  xmlns="http://www.w3.org/2000/svg"  width="24"  height="24"  viewBox="0 0 24 24"  fill="none"  stroke="currentColor"  stroke-width="2"  stroke-linecap="round"  stroke-linejoin="round"  class="icon icon-tabler icons-tabler-outline icon-tabler-check"><path stroke="none" d="M0 0h24v24H0z" fill="none"/><path d="M5 12l5 5l10 -10" /></svg>
`;
const checkIcon = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.LabIcon({
    name: 'my-variable-check-icon',
    svgstr: svgStr
});


/***/ }),

/***/ "./lib/icons/detailIcon.js":
/*!*********************************!*\
  !*** ./lib/icons/detailIcon.js ***!
  \*********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   detailIcon: () => (/* binding */ detailIcon)
/* harmony export */ });
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__);

const svgStr = `
<svg  xmlns="http://www.w3.org/2000/svg"  width="24"  height="24"  viewBox="0 0 24 24"  fill="none"  stroke="currentColor"  stroke-width="2"  stroke-linecap="round"  stroke-linejoin="round"  class="icon icon-tabler icons-tabler-outline icon-tabler-matrix"><path stroke="none" d="M0 0h24v24H0z" fill="none"/><path d="M8 16h.013" /><path d="M12.01 16h.005" /><path d="M16.015 16h.005" /><path d="M16.015 12h.005" /><path d="M8.01 12h.005" /><path d="M12.01 12h.005" /><path d="M16.02 8h.005" /><path d="M8.015 8h.005" /><path d="M12.015 8h.005" /><path d="M7 4h-1a2 2 0 0 0 -2 2v12a2 2 0 0 0 2 2h1" /><path d="M17 4h1a2 2 0 0 1 2 2v12a2 2 0 0 1 -2 2h-1" /></svg>
`;
const detailIcon = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.LabIcon({
    name: 'detail-plugin-icon',
    svgstr: svgStr,
});


/***/ }),

/***/ "./lib/icons/panelIcon.js":
/*!********************************!*\
  !*** ./lib/icons/panelIcon.js ***!
  \********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   panelIcon: () => (/* binding */ panelIcon)
/* harmony export */ });
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__);

const svgStr = `
<svg  xmlns="http://www.w3.org/2000/svg"  width="24"  height="24"  viewBox="0 0 24 24"  fill="none"  stroke="currentColor"  stroke-width="2"  stroke-linecap="round"  stroke-linejoin="round"  class="icon icon-tabler icons-tabler-outline icon-tabler-table-export"><path stroke="none" d="M0 0h24v24H0z" fill="none"/><path d="M12.5 21h-7.5a2 2 0 0 1 -2 -2v-14a2 2 0 0 1 2 -2h14a2 2 0 0 1 2 2v7.5" /><path d="M3 10h18" /><path d="M10 3v18" /><path d="M16 19h6" /><path d="M19 16l3 3l-3 3" /></svg>
`;
const panelIcon = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.LabIcon({
    name: 'inspector-panel-icon',
    svgstr: svgStr,
});


/***/ }),

/***/ "./lib/icons/pluginIcon.js":
/*!*********************************!*\
  !*** ./lib/icons/pluginIcon.js ***!
  \*********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   pluginIcon: () => (/* binding */ pluginIcon)
/* harmony export */ });
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__);

const svgStr = `
<svg  xmlns="http://www.w3.org/2000/svg"  width="24"  height="24"  viewBox="0 0 24 24"  fill="none"  stroke="currentColor"  stroke-width="2"  stroke-linecap="round"  stroke-linejoin="round"  class="icon icon-tabler icons-tabler-outline icon-tabler-variable"><path stroke="none" d="M0 0h24v24H0z" fill="none"/><path d="M5 4c-2.5 5 -2.5 10 0 16m14 -16c2.5 5 2.5 10 0 16m-10 -11h1c1 0 1 1 2.016 3.527c.984 2.473 .984 3.473 1.984 3.473h1" /><path d="M8 16c1.5 0 3 -2 4 -3.5s2.5 -3.5 4 -3.5" /></svg>
`;
const pluginIcon = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.LabIcon({
    name: 'variable-plugin-icon',
    svgstr: svgStr,
});


/***/ }),

/***/ "./lib/icons/refreshIcon.js":
/*!**********************************!*\
  !*** ./lib/icons/refreshIcon.js ***!
  \**********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   refreshIcon: () => (/* binding */ refreshIcon)
/* harmony export */ });
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__);

const svgStr = `
<svg  xmlns="http://www.w3.org/2000/svg"  width="24"  height="24"  viewBox="0 0 24 24"  fill="none"  stroke="currentColor"  stroke-width="2"  stroke-linecap="round"  stroke-linejoin="round"  class="icon icon-tabler icons-tabler-outline icon-tabler-refresh"><path stroke="none" d="M0 0h24v24H0z" fill="none"/><path d="M20 11a8.1 8.1 0 0 0 -15.5 -2m-.5 -4v4h4" /><path d="M4 13a8.1 8.1 0 0 0 15.5 2m.5 4v-4h-4" /></svg>
`;
const refreshIcon = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.LabIcon({
    name: 'my-variable-refresh-icon',
    svgstr: svgStr
});


/***/ }),

/***/ "./lib/icons/settingsIcon.js":
/*!***********************************!*\
  !*** ./lib/icons/settingsIcon.js ***!
  \***********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   settingsIcon: () => (/* binding */ settingsIcon)
/* harmony export */ });
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__);

const svgStr = `
<svg  xmlns="http://www.w3.org/2000/svg"  width="24"  height="24"  viewBox="0 0 24 24"  fill="none"  stroke="currentColor"  stroke-width="2"  stroke-linecap="round"  stroke-linejoin="round"  class="icon icon-tabler icons-tabler-outline icon-tabler-settings"><path stroke="none" d="M0 0h24v24H0z" fill="none"/><path d="M10.325 4.317c.426 -1.756 2.924 -1.756 3.35 0a1.724 1.724 0 0 0 2.573 1.066c1.543 -.94 3.31 .826 2.37 2.37a1.724 1.724 0 0 0 1.065 2.572c1.756 .426 1.756 2.924 0 3.35a1.724 1.724 0 0 0 -1.066 2.573c.94 1.543 -.826 3.31 -2.37 2.37a1.724 1.724 0 0 0 -2.572 1.065c-.426 1.756 -2.924 1.756 -3.35 0a1.724 1.724 0 0 0 -2.573 -1.066c-1.543 .94 -3.31 -.826 -2.37 -2.37a1.724 1.724 0 0 0 -1.065 -2.572c-1.756 -.426 -1.756 -2.924 0 -3.35a1.724 1.724 0 0 0 1.066 -2.573c-.94 -1.543 .826 -3.31 2.37 -2.37c1 .608 2.296 .07 2.572 -1.065z" /><path d="M9 12a3 3 0 1 0 6 0a3 3 0 0 0 -6 0" /></svg>
`;
const settingsIcon = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.LabIcon({
    name: 'my-variable-settings-icon',
    svgstr: svgStr
});


/***/ }),

/***/ "./lib/icons/skipLeftIcon.js":
/*!***********************************!*\
  !*** ./lib/icons/skipLeftIcon.js ***!
  \***********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   skipLeftIcon: () => (/* binding */ skipLeftIcon)
/* harmony export */ });
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__);

const svgStr = `
<svg  xmlns="http://www.w3.org/2000/svg"  width="24"  height="24"  viewBox="0 0 24 24"  fill="none"  stroke="currentColor"  stroke-width="2"  stroke-linecap="round"  stroke-linejoin="round"  class="icon icon-tabler icons-tabler-outline icon-tabler-chevrons-left"><path stroke="none" d="M0 0h24v24H0z" fill="none"/><path d="M11 7l-5 5l5 5" /><path d="M17 7l-5 5l5 5" /></svg>
`;
const skipLeftIcon = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.LabIcon({
    name: 'my-variable-skip-left-icon',
    svgstr: svgStr
});


/***/ }),

/***/ "./lib/icons/skipRightIcon.js":
/*!************************************!*\
  !*** ./lib/icons/skipRightIcon.js ***!
  \************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   skipRightIcon: () => (/* binding */ skipRightIcon)
/* harmony export */ });
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__);

const svgStr = `
<svg  xmlns="http://www.w3.org/2000/svg"  width="24"  height="24"  viewBox="0 0 24 24"  fill="none"  stroke="currentColor"  stroke-width="2"  stroke-linecap="round"  stroke-linejoin="round"  class="icon icon-tabler icons-tabler-outline icon-tabler-chevrons-right"><path stroke="none" d="M0 0h24v24H0z" fill="none"/><path d="M7 7l5 5l-5 5" /><path d="M13 7l5 5l-5 5" /></svg>
`;
const skipRightIcon = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.LabIcon({
    name: 'my-variable-skip-right-icon',
    svgstr: svgStr
});


/***/ }),

/***/ "./lib/icons/smallSkipLeftIcon.js":
/*!****************************************!*\
  !*** ./lib/icons/smallSkipLeftIcon.js ***!
  \****************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   smallSkipLeftIcon: () => (/* binding */ smallSkipLeftIcon)
/* harmony export */ });
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__);

const svgStr = `
<svg  xmlns="http://www.w3.org/2000/svg"  width="24"  height="24"  viewBox="0 0 24 24"  fill="none"  stroke="currentColor"  stroke-width="2"  stroke-linecap="round"  stroke-linejoin="round"  class="icon icon-tabler icons-tabler-outline icon-tabler-chevron-left"><path stroke="none" d="M0 0h24v24H0z" fill="none"/><path d="M15 6l-6 6l6 6" /></svg>`;
const smallSkipLeftIcon = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.LabIcon({
    name: 'mljar-variable-inspector-small-skip-left-icon',
    svgstr: svgStr
});


/***/ }),

/***/ "./lib/icons/smallSkipRightIcon.js":
/*!*****************************************!*\
  !*** ./lib/icons/smallSkipRightIcon.js ***!
  \*****************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   smallSkipRightIcon: () => (/* binding */ smallSkipRightIcon)
/* harmony export */ });
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__);

const svgStr = `
<svg  xmlns="http://www.w3.org/2000/svg"  width="24"  height="24"  viewBox="0 0 24 24"  fill="none"  stroke="currentColor"  stroke-width="2"  stroke-linecap="round"  stroke-linejoin="round"  class="icon icon-tabler icons-tabler-outline icon-tabler-chevron-right"><path stroke="none" d="M0 0h24v24H0z" fill="none"/><path d="M9 6l6 6l-6 6" /></svg>`;
const smallSkipRightIcon = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.LabIcon({
    name: 'mljar-variable-inspector-small-skip-right-icon',
    svgstr: svgStr
});


/***/ }),

/***/ "./lib/index.js":
/*!**********************!*\
  !*** ./lib/index.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   VARIABLE_INSPECTOR_ID: () => (/* binding */ VARIABLE_INSPECTOR_ID),
/* harmony export */   autoRefreshProperty: () => (/* binding */ autoRefreshProperty),
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__),
/* harmony export */   showShapeProperty: () => (/* binding */ showShapeProperty),
/* harmony export */   showSizeProperty: () => (/* binding */ showSizeProperty),
/* harmony export */   showTypeProperty: () => (/* binding */ showTypeProperty)
/* harmony export */ });
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/application */ "webpack/sharing/consume/default/@jupyterlab/application");
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/settingregistry */ "webpack/sharing/consume/default/@jupyterlab/settingregistry");
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_statedb__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/statedb */ "webpack/sharing/consume/default/@jupyterlab/statedb");
/* harmony import */ var _jupyterlab_statedb__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_statedb__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _components_variableInspectorSidebar__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./components/variableInspectorSidebar */ "./lib/components/variableInspectorSidebar.js");
/* harmony import */ var _watchers_notebookWatcher__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./watchers/notebookWatcher */ "./lib/watchers/notebookWatcher.js");





const VARIABLE_INSPECTOR_ID = 'variable-inspector:plugin';
const autoRefreshProperty = 'variableInspectorAutoRefresh';
const showTypeProperty = 'variableInspectorShowType';
const showShapeProperty = 'variableInspectorShowShape';
const showSizeProperty = 'variableInspectorShowSize';
const leftTab = {
    id: VARIABLE_INSPECTOR_ID,
    description: 'A JupyterLab extension to easy manage variables.',
    autoStart: true,
    requires: [_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILabShell, _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_1__.ISettingRegistry, _jupyterlab_statedb__WEBPACK_IMPORTED_MODULE_2__.IStateDB],
    activate: async (app, labShell, settingregistry, stateDB) => {
        const notebookWatcher = new _watchers_notebookWatcher__WEBPACK_IMPORTED_MODULE_3__.NotebookWatcher(app.shell);
        const widget = (0,_components_variableInspectorSidebar__WEBPACK_IMPORTED_MODULE_4__.createVariableInspectorSidebar)(notebookWatcher, app.commands, labShell, settingregistry, stateDB);
        app.shell.add(widget, 'left', { rank: 1998 });
    }
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = ([leftTab]);


/***/ }),

/***/ "./lib/python_code/getMatrix.js":
/*!**************************************!*\
  !*** ./lib/python_code/getMatrix.js ***!
  \**************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   getMatrix: () => (/* binding */ getMatrix)
/* harmony export */ });
const getMatrix = (varName, startRow, endRow, startColumn, endColumn) => `
import importlib
from IPython.display import JSON

def __get_variable_shape(obj):
    if hasattr(obj, 'shape'):
        return " x ".join(map(str, obj.shape))
    if isinstance(obj, list):
        if obj and all(isinstance(el, list) for el in obj):
            if len(set(map(len, obj))) == 1:
                return f"{len(obj)} x {len(obj[0])}"
            else:
                return f"{len(obj)}"
        return str(len(obj))
    return ""

def __format_content(item):
    if isinstance(item, list):
        return [__format_content(subitem) for subitem in item]
    elif isinstance(item, dict):
        return {k: __format_content(v) for k, v in item.items()}
    elif isinstance(item, str):
        return item[:50] + "..." if len(item) > 50 else item
    elif isinstance(item, (int, float, bool)) or item is None:
        return item
    else:
        if hasattr(item, "name"):
            return getattr(item, "name")
        return type(item).__name__

def __mljar_variable_inspector_get_matrix_content(
    var_name="${varName}",
    start_row=${startRow},
    end_row=${endRow},
    start_column=${startColumn},
    end_column=${endColumn}
):
    if var_name not in globals():
        return JSON({"error": "Variable not found."})
    
    obj = globals()[var_name]
    module_name = type(obj).__module__
    var_type = type(obj).__name__
    var_shape = __get_variable_shape(obj)
    
    if "numpy" in module_name:
        try:
            np = importlib.import_module("numpy")
        except ImportError:
            return JSON({"error": "Numpy is not installed."})
        if isinstance(obj, np.ndarray):
            if obj.ndim > 2:
                return JSON({
                    "variable": var_name,
                    "variableType": var_type,
                    "variableShape": var_shape,
                    "error": "Numpy array has more than 2 dimensions."
                })
            if obj.ndim == 1:
                actual_end_row = min(end_row, len(obj))
                sliced = obj[start_row:actual_end_row]
                returnedSize = [start_row, actual_end_row, 0, 1]
            else:
                actual_end_row = min(end_row, obj.shape[0])
                actual_end_column = min(end_column, obj.shape[1])
                sliced = obj[start_row:actual_end_row, start_column:actual_end_column]
                returnedSize = [start_row, actual_end_row, start_column, actual_end_column]
            return JSON({
                "variable": var_name,
                "variableType": var_type,
                "variableShape": var_shape,
                "returnedSize": returnedSize,
                "content": __format_content(sliced.tolist())
            })
    
    if "pandas" in module_name:
        try:
            pd = importlib.import_module("pandas")
        except ImportError:
            return JSON({"error": "Pandas is not installed."})
        if isinstance(obj, pd.DataFrame):
            actual_end_row = min(end_row, len(obj.index))
            actual_end_column = min(end_column, len(obj.columns))
            sliced = obj.iloc[start_row:actual_end_row, start_column:actual_end_column]
            result = []
            for col in sliced.columns:
                col_values = [col] + sliced[col].tolist()
                result.append(col_values)
            returnedSize = [start_row, actual_end_row, start_column, actual_end_column]
            return JSON({
                "variable": var_name,
                "variableType": var_type,
                "variableShape": var_shape,
                "returnedSize": returnedSize,
                "content": __format_content(result)
            })
        elif isinstance(obj, pd.Series):
            actual_end_row = min(end_row, len(obj))
            sliced = obj.iloc[start_row:actual_end_row]
            df = sliced.to_frame()
            result = []
            for col in df.columns:
                col_values = [col] + df[col].tolist()
                result.append(col_values)
            returnedSize = [start_row, actual_end_row, 0, 1]
            return JSON({
                "variable": var_name,
                "variableType": var_type,
                "variableShape": var_shape,
                "returnedSize": returnedSize,
                "content": __format_content(result)
            })
    
    if isinstance(obj, list):
        if all(isinstance(el, list) for el in obj):
            if len(set(map(len, obj))) == 1:
                actual_end_row = min(end_row, len(obj))
                actual_end_column = min(end_column, len(obj[0]))
                sliced = [row[start_column:actual_end_column] for row in obj[start_row:actual_end_row]]
                returnedSize = [start_row, actual_end_row, start_column, actual_end_column]
                content = __format_content(sliced)
            else:
                actual_end_row = min(end_row, len(obj))
                sliced = obj[start_row:actual_end_row]
                returnedSize = [start_row, actual_end_row, 0, 1]
                content = ["list" for _ in sliced]
                var_shape = f"{len(obj)}"
            return JSON({
                "variable": var_name,
                "variableType": var_type,
                "variableShape": var_shape,
                "returnedSize": returnedSize,
                "content": content
            })
        else:
            actual_end_row = min(end_row, len(obj))
            sliced = obj[start_row:actual_end_row]
            returnedSize = [start_row, actual_end_row, 0, 1]
            return JSON({
                "variable": var_name,
                "variableType": var_type,
                "variableShape": str(len(obj)),
                "returnedSize": returnedSize,
                "content": __format_content(sliced)
            })
    
    if isinstance(obj, dict):
        items = list(obj.items())[start_row:end_row]
        sliced_dict = dict(items)
        returnedSize = [start_row, end_row, 0, 1]
        var_shape = str(len(obj))
        return JSON({
            "variable": var_name,
            "variableType": var_type,
            "variableShape": var_shape,
            "returnedSize": returnedSize,
            "content": __format_content(sliced_dict)
        })
    
    return JSON({
        "variable": var_name,
        "variableType": var_type,
        "variableShape": "unknown",
        "error": "Variable is not a supported array type.",
        "content": [10, 10, 10]  
    })

__mljar_variable_inspector_get_matrix_content()
`;


/***/ }),

/***/ "./lib/python_code/getVariables.js":
/*!*****************************************!*\
  !*** ./lib/python_code/getVariables.js ***!
  \*****************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   variableDict: () => (/* binding */ variableDict)
/* harmony export */ });
const variableDict = `
import json
import sys
import math
from importlib import __import__
from IPython import get_ipython
from IPython.core.magics.namespace import NamespaceMagics

__mljar_variable_inspector_nms = NamespaceMagics()
__mljar_variable_inspector_Jupyter = get_ipython()
__mljar_variable_inspector_nms.shell = __mljar_variable_inspector_Jupyter.kernel.shell

__np = None
__pd = None
__pyspark = None
__tf = None
__K = None
__torch = None
__ipywidgets = None
__xr = None


def __mljar_variable_inspector_attempt_import(module):
    try:
        return __import__(module)
    except ImportError:
        return None


def __mljar_variable_inspector_check_imported():
    global __np, __pd, __pyspark, __tf, __K, __torch, __ipywidgets, __xr

    __np = __mljar_variable_inspector_attempt_import('numpy')
    __pd = __mljar_variable_inspector_attempt_import('pandas')
    __pyspark = __mljar_variable_inspector_attempt_import('pyspark')
    __tf = __mljar_variable_inspector_attempt_import('tensorflow')
    __K = __mljar_variable_inspector_attempt_import('keras.backend') or __mljar_variable_inspector_attempt_import('tensorflow.keras.backend')
    __torch = __mljar_variable_inspector_attempt_import('torch')
    __ipywidgets = __mljar_variable_inspector_attempt_import('ipywidgets')
    __xr = __mljar_variable_inspector_attempt_import('xarray')


def __mljar_variable_inspector_getshapeof(x):
    def get_list_shape(lst):
        if isinstance(lst, list):
            if not lst:
                return "0"
            sub_shape = get_list_shape(lst[0])
            return f"{len(lst)}" if sub_shape == "" else f"{len(lst)} x {sub_shape}"
        else:
            return ""

    if __pd and isinstance(x, __pd.DataFrame):
        return "%d x %d" % x.shape
    if __pd and isinstance(x, __pd.Series):
        return "%d" % x.shape
    if __np and isinstance(x, __np.ndarray):
        shape = " x ".join([str(i) for i in x.shape])
        return "%s" % shape
    if __pyspark and isinstance(x, __pyspark.sql.DataFrame):
        return "? x %d" % len(x.columns)
    if __tf and isinstance(x, __tf.Variable):
        shape = " x ".join([str(int(i)) for i in x.shape])
        return "%s" % shape
    if __tf and isinstance(x, __tf.Tensor):
        shape = " x ".join([str(int(i)) for i in x.shape])
        return "%s" % shape
    if __torch and isinstance(x, __torch.Tensor):
        shape = " x ".join([str(int(i)) for i in x.shape])
        return "%s" % shape
    if __xr and isinstance(x, __xr.DataArray):
        shape = " x ".join([str(int(i)) for i in x.shape])
        return "%s" % shape
    if isinstance(x, list):
        return get_list_shape(x)
    if isinstance(x, dict):
        return "%s keys" % len(x)
    return None


def __format_content(item):
    if isinstance(item, list):
        return __format_content(str([__format_content(subitem) for subitem in item]))
    elif isinstance(item, dict):
        return __format_content(str({k: __format_content(v) for k, v in item.items()}))
    elif isinstance(item, str):
        return item[:100] + "..." if len(item) > 100 else item
    elif isinstance(item, (int, float, bool, set)) or item is None:
        return item
    else:
        if hasattr(item, "name"):
            return getattr(item, "name")
        return type(item).__name__   

def __mljar_variable_inspector_get_simple_value(x):
    if isinstance(x, bytes):
        return ""
    if x is None:
        return "None"
    if __np is not None and __np.isscalar(x) and not isinstance(x, bytes):
        return str(x)
    if isinstance(x, (int, float, complex, bool, str, set, list, dict)):
        strValue = str(x) #__format_content(x)
        if len(strValue) > 100:
            return strValue[:100] + "..."
        else:
            return strValue
    # if isinstance(x, (list, dict)):
    #     return __format_content(x)

    return ""


def __mljar_variable_inspector_size_converter(size):
    if size == 0: 
        return '0B'
    units = ['B', 'kB', 'MB', 'GB', 'TB']
    index = math.floor(math.log(size, 1024))
    divider = math.pow(1024, index)
    converted_size = round(size / divider, 2)
    return f"{converted_size} {units[index]}"


def __mljar_variable_inspector_dict_list():
    __mljar_variable_inspector_check_imported()
    def __mljar_variable_inspector_keep_cond(v):
        try:
            obj = eval(v)
            if isinstance(obj, str):
                return True
            if __tf and isinstance(obj, __tf.Variable):
                return True
            if __pd and __pd is not None and (
                isinstance(obj, __pd.core.frame.DataFrame)
                or isinstance(obj, __pd.core.series.Series)):
                return True
            if __xr and __xr is not None and isinstance(obj, __xr.DataArray):
                return True
            if str(obj).startswith("<psycopg.Connection"):
                return True
            if str(obj).startswith("<module"):
                return False
            if str(obj).startswith("<class"):
                return False 
            if str(obj).startswith("<function"):
                return False 
            if  v in ['__np', '__pd', '__pyspark', '__tf', '__K', '__torch', '__ipywidgets', '__xr']:
                return obj is not None
            if str(obj).startswith("_Feature"):
                # removes tf/keras objects
                return False
            return True
        except:
            return False
    values = __mljar_variable_inspector_nms.who_ls()
    
    vardic = []
    for _v in values:
        if __mljar_variable_inspector_keep_cond(_v):
            _ev = eval(_v)
            vardic += [{
                'varName': _v,
                'varType': type(_ev).__name__, 
                'varShape': str(__mljar_variable_inspector_getshapeof(_ev)) if __mljar_variable_inspector_getshapeof(_ev) else '',
                'varDimension': __mljar_variable_inspector_getdim(_ev),
                'varSize': __mljar_variable_inspector_size_converter(__mljar_variable_inspector_get_size_mb(_ev)),
                'varSimpleValue': __mljar_variable_inspector_get_simple_value(_ev)
            }]
    # from IPython.display import JSON
    # return JSON(vardic)
    return json.dumps(vardic, ensure_ascii=False)


def __mljar_variable_inspector_get_size_mb(obj):
    return sys.getsizeof(obj)


def __mljar_variable_inspector_getdim(x):
    """
    return dimension for object:
      - For Data frame -> 2
      - For Series -> 1
      - For NDarray -> korzysta z atrybutu ndim
      - For pyspark DataFrame -> 2
      - For TensorFlow, PyTorch, xarray -> shape length
      - For list -> nesting depth
      - For sklar type (int, float, itp.) -> 1
      - For other objects or dict -> 0
    """
    if __pd and isinstance(x, __pd.DataFrame):
        return 2
    if __pd and isinstance(x, __pd.Series):
        return 1
    if __np and isinstance(x, __np.ndarray):
        return x.ndim
    if __pyspark and isinstance(x, __pyspark.sql.DataFrame):
        return 2
    if __tf and (isinstance(x, __tf.Variable) or isinstance(x, __tf.Tensor)):
        try:
            return len(x.shape)
        except Exception:
            return 0
    if __torch and isinstance(x, __torch.Tensor):
        return len(x.shape)
    if __xr and isinstance(x, __xr.DataArray):
        return len(x.shape)
    if isinstance(x, list):
        def __mljar_variable_inspector_list_depth(lst):
            if isinstance(lst, list) and lst:
                subdepths = [__mljar_variable_inspector_list_depth(el) for el in lst if isinstance(el, list)]
                if subdepths:
                    return 1 + max(subdepths)
                else:
                    return 1
            else:
                return 0
        return __mljar_variable_inspector_list_depth(x)
    if isinstance(x, (int, float, complex, bool, str)):
        return 1
    if isinstance(x, dict):
        return 0
    return 0


def __mljar_variable_inspector_getmatrixcontent(x, max_rows=10000):
    # to do: add something to handle this in the future
    threshold = max_rows

    if __pd and __pyspark and isinstance(x, __pyspark.sql.DataFrame):
        df = x.limit(threshold).toPandas()
        return __mljar_variable_inspector_getmatrixcontent(df.copy())
    elif __np and __pd and type(x).__name__ == "DataFrame":
        if threshold is not None:
            x = x.head(threshold)
        x.columns = x.columns.map(str)
        return x.to_json(orient="table", default_handler= __mljar_variable_inspector_default, force_ascii=False)
    elif __np and __pd and type(x).__name__ == "Series": 
        if threshold is not None:
            x = x.head(threshold)
        return x.to_json(orient="table", default_handler= __mljar_variable_inspector_default, force_ascii=False)
    elif __np and __pd and type(x).__name__ == "ndarray":
        df = __pd.DataFrame(x)
        return __mljar_variable_inspector_getmatrixcontent(df)
    elif __tf and (isinstance(x, __tf.Variable) or isinstance(x, __tf.Tensor)):
        df = __K.get_value(x)
        return __mljar_variable_inspector_getmatrixcontent(df)
    elif __torch and isinstance(x, __torch.Tensor):
        df = x.cpu().numpy()
        return __mljar_variable_inspector_getmatrixcontent(df)
    elif __xr and isinstance(x, __xr.DataArray):
        df = x.to_numpy()
        return __mljar_variable_inspector_getmatrixcontent(df)
    elif isinstance(x, list):
        s = __pd.Series(x)
        return __mljar_variable_inspector_getmatrixcontent(s)


def __mljar_variable_inspector_displaywidget(widget):
    display(widget)


def __mljar_variable_inspector_default(o):
    if isinstance(o, __np.number): return int(o)  
    raise TypeError


def __mljar_variable_inspector_deletevariable(x):
    exec("del %s" % x, globals())

__mljar_variable_inspector_dict_list()
`;


/***/ }),

/***/ "./lib/utils/allowedTypes.js":
/*!***********************************!*\
  !*** ./lib/utils/allowedTypes.js ***!
  \***********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   allowedTypes: () => (/* binding */ allowedTypes)
/* harmony export */ });
const allowedTypes = ['ndarray', 'DataFrame', 'list', 'Series', 'tuple'];


/***/ }),

/***/ "./lib/utils/executeGetMatrix.js":
/*!***************************************!*\
  !*** ./lib/utils/executeGetMatrix.js ***!
  \***************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   executeMatrixContent: () => (/* binding */ executeMatrixContent)
/* harmony export */ });
/* harmony import */ var _python_code_getMatrix__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../python_code/getMatrix */ "./lib/python_code/getMatrix.js");

const executeMatrixContent = async (varName, varStartColumn, varEndColumn, varStartRow, varEndRow, notebookPanel) => {
    if (!notebookPanel) {
        throw new Error('Kernel not available.');
    }
    const code = (0,_python_code_getMatrix__WEBPACK_IMPORTED_MODULE_0__.getMatrix)(varName, varStartRow, varEndRow, varStartColumn, varEndColumn);
    return new Promise((resolve, reject) => {
        var _a, _b, _c;
        let outputData = '';
        let resultResolved = false;
        const future = (_c = (_b = (_a = notebookPanel.sessionContext) === null || _a === void 0 ? void 0 : _a.session) === null || _b === void 0 ? void 0 : _b.kernel) === null || _c === void 0 ? void 0 : _c.requestExecute({
            code,
            store_history: false
        });
        if (!future) {
            return reject(new Error('No future returned from kernel execution.'));
        }
        future.onIOPub = (msg) => {
            const msgType = msg.header.msg_type;
            if (msgType === 'execute_result' || msgType === 'display_data') {
                const content = msg.content;
                if (content.data && content.data['application/json']) {
                    resultResolved = true;
                    resolve(content.data['application/json']);
                }
                else if (content.data && content.data['text/plain']) {
                    outputData += content.data['text/plain'];
                }
            }
            else if (msgType === 'stream') {
                /* empty */
            }
            else if (msgType === 'error') {
                console.error('Python error:', msg.content);
                reject(new Error('Error during Python execution.'));
            }
        };
        future.done.then(() => {
            if (!resultResolved) {
                try {
                    const cleanedData = outputData.trim();
                    const parsed = JSON.parse(cleanedData);
                    resolve(parsed);
                }
                catch (err) {
                    reject(new Error('Failed to parse output from Python.'));
                }
            }
        });
    });
};


/***/ }),

/***/ "./lib/utils/kernelOperationNotifier.js":
/*!**********************************************!*\
  !*** ./lib/utils/kernelOperationNotifier.js ***!
  \**********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   KernelOperationNotifier: () => (/* binding */ KernelOperationNotifier),
/* harmony export */   kernelOperationNotifier: () => (/* binding */ kernelOperationNotifier),
/* harmony export */   withIgnoredPanelKernelUpdates: () => (/* binding */ withIgnoredPanelKernelUpdates),
/* harmony export */   withIgnoredSidebarKernelUpdates: () => (/* binding */ withIgnoredSidebarKernelUpdates)
/* harmony export */ });
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/signaling */ "webpack/sharing/consume/default/@lumino/signaling");
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_signaling__WEBPACK_IMPORTED_MODULE_0__);

class KernelOperationNotifier {
    constructor() {
        this._inProgressSidebar = false;
        this._inProgressPanel = false;
        this.sidebarOperationChanged = new _lumino_signaling__WEBPACK_IMPORTED_MODULE_0__.Signal(this);
        this.panelOperationChanged = new _lumino_signaling__WEBPACK_IMPORTED_MODULE_0__.Signal(this);
    }
    set inProgressSidebar(value) {
        if (this._inProgressSidebar !== value) {
            this._inProgressSidebar = value;
            this.sidebarOperationChanged.emit(value);
        }
    }
    get inProgressSidebar() {
        return this._inProgressSidebar;
    }
    set inProgressPanel(value) {
        if (this._inProgressPanel !== value) {
            this._inProgressPanel = value;
            this.panelOperationChanged.emit(value);
        }
    }
    get inProgressPanel() {
        return this._inProgressPanel;
    }
}
const kernelOperationNotifier = new KernelOperationNotifier();
async function withIgnoredSidebarKernelUpdates(fn) {
    kernelOperationNotifier.inProgressSidebar = true;
    try {
        return await fn();
    }
    finally {
        kernelOperationNotifier.inProgressSidebar = false;
    }
}
async function withIgnoredPanelKernelUpdates(fn) {
    kernelOperationNotifier.inProgressPanel = true;
    try {
        return await fn();
    }
    finally {
        kernelOperationNotifier.inProgressPanel = false;
    }
}


/***/ }),

/***/ "./lib/utils/utils.js":
/*!****************************!*\
  !*** ./lib/utils/utils.js ***!
  \****************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   transformMatrixData: () => (/* binding */ transformMatrixData),
/* harmony export */   transpose: () => (/* binding */ transpose)
/* harmony export */ });
/* harmony import */ var _allowedTypes__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./allowedTypes */ "./lib/utils/allowedTypes.js");

function transpose(matrix) {
    return matrix[0].map((_, colIndex) => matrix.map((row) => row[colIndex]));
}
function transformMatrixData(matrixData, variableType, currentRow, currentColumn) {
    let data2D = [];
    if (matrixData.length > 0 && !Array.isArray(matrixData[0])) {
        data2D = matrixData.map(item => [item]);
    }
    else {
        data2D = matrixData;
    }
    let data = data2D;
    let fixedRowCount = 0;
    let fixedColumnCount = 0;
    if (data2D.length > 0 && _allowedTypes__WEBPACK_IMPORTED_MODULE_0__.allowedTypes.includes(variableType)) {
        const globalRowStart = currentRow;
        const headerRow = ['index'];
        const headerLength = variableType === 'DataFrame' ? data2D[0].length - 1 : data2D[0].length;
        for (let j = 0; j < headerLength; j++) {
            headerRow.push((globalRowStart + j).toString());
        }
        let newData = [headerRow];
        for (let i = 0; i < data2D.length; i++) {
            if (variableType === 'DataFrame') {
                newData.push([...data2D[i]]);
            }
            else {
                const globalIndex = currentRow + i;
                newData.push([globalIndex, ...data2D[i]]);
            }
        }
        if (variableType === 'DataFrame' || variableType === 'Series') {
            newData = transpose(newData);
        }
        data2D = transpose(data2D);
        data = newData;
        fixedRowCount = 1;
        fixedColumnCount = 1;
    }
    return { data, fixedRowCount, fixedColumnCount };
}


/***/ }),

/***/ "./lib/watchers/notebookWatcher.js":
/*!*****************************************!*\
  !*** ./lib/watchers/notebookWatcher.js ***!
  \*****************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   NotebookWatcher: () => (/* binding */ NotebookWatcher)
/* harmony export */ });
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/notebook */ "webpack/sharing/consume/default/@jupyterlab/notebook");
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @lumino/signaling */ "webpack/sharing/consume/default/@lumino/signaling");
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_lumino_signaling__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_docregistry__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/docregistry */ "webpack/sharing/consume/default/@jupyterlab/docregistry");
/* harmony import */ var _jupyterlab_docregistry__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_docregistry__WEBPACK_IMPORTED_MODULE_2__);




function getNotebook(widget) {
    if (!(widget instanceof _jupyterlab_docregistry__WEBPACK_IMPORTED_MODULE_2__.DocumentWidget)) {
        return null;
    }
    const { content } = widget;
    if (!(content instanceof _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__.Notebook)) {
        return null;
    }
    return content;
}
class NotebookWatcher {
    constructor(shell) {
        var _a;
        this._kernelInfo = null;
        this._kernelChanged = new _lumino_signaling__WEBPACK_IMPORTED_MODULE_1__.Signal(this);
        this._mainAreaWidget = null;
        this._notebookPanel = null;
        this._notebookPanelChanged = new _lumino_signaling__WEBPACK_IMPORTED_MODULE_1__.Signal(this);
        this._shell = shell;
        (_a = this._shell.currentChanged) === null || _a === void 0 ? void 0 : _a.connect((sender, args) => {
            this._mainAreaWidget = args.newValue;
            this._notebookPanel = this.notebookPanel();
            this._notebookPanelChanged.emit(this._notebookPanel);
            this._attachKernelChangeHandler();
        });
    }
    get notebookPanelChanged() {
        return this._notebookPanelChanged;
    }
    get kernelInfo() {
        return this._kernelInfo;
    }
    get kernelChanged() {
        return this._kernelChanged;
    }
    notebookPanel() {
        const notebook = getNotebook(this._mainAreaWidget);
        if (!notebook) {
            return null;
        }
        return notebook.parent instanceof _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__.NotebookPanel ? notebook.parent : null;
    }
    _attachKernelChangeHandler() {
        if (this._notebookPanel) {
            const session = this._notebookPanel.sessionContext.session;
            if (session) {
                session.kernelChanged.connect(this._onKernelChanged, this);
                this._updateKernelInfo(session.kernel);
            }
            else {
                setTimeout(() => {
                    var _a;
                    const delayedSession = (_a = this._notebookPanel) === null || _a === void 0 ? void 0 : _a.sessionContext.session;
                    if (delayedSession) {
                        delayedSession.kernelChanged.connect(this._onKernelChanged, this);
                        this._updateKernelInfo(delayedSession.kernel);
                    }
                    else {
                        console.warn('Session not initialized after delay');
                    }
                }, 2000);
            }
        }
        else {
            console.warn('Session not initalizated');
        }
    }
    _onKernelChanged(sender, args) {
        if (args.newValue) {
            this._updateKernelInfo(args.newValue);
        }
        else {
            this._kernelInfo = null;
            this._kernelChanged.emit(null);
        }
    }
    _updateKernelInfo(kernel) {
        this._kernelInfo = {
            name: kernel.name,
            id: kernel.id
        };
        this._kernelChanged.emit(this._kernelInfo);
    }
}


/***/ })

}]);
//# sourceMappingURL=lib_index_js.36552d52fdcf8c18b714.js.map