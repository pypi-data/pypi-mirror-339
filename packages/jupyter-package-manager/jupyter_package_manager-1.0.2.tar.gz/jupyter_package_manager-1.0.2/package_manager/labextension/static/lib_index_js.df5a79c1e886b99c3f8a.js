"use strict";
(self["webpackChunkjupyter_package_manager"] = self["webpackChunkjupyter_package_manager"] || []).push([["lib_index_js"],{

/***/ "./lib/components/backButton.js":
/*!**************************************!*\
  !*** ./lib/components/backButton.js ***!
  \**************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   BackButton: () => (/* binding */ BackButton)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _icons_backIcon__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../icons/backIcon */ "./lib/icons/backIcon.js");


const BackButton = ({ onBack }) => {
    return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("button", { className: "mljar-packages-manager-back-button", onClick: onBack, title: "Go Back" },
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_icons_backIcon__WEBPACK_IMPORTED_MODULE_1__.backIcon.react, { className: "mljar-packages-manager-back-icon" }),
        "Back"));
};


/***/ }),

/***/ "./lib/components/installButton.js":
/*!*****************************************!*\
  !*** ./lib/components/installButton.js ***!
  \*****************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   InstallButton: () => (/* binding */ InstallButton)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _contexts_packagesListContext__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../contexts/packagesListContext */ "./lib/contexts/packagesListContext.js");
/* harmony import */ var _icons_installPackageIcon__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../icons/installPackageIcon */ "./lib/icons/installPackageIcon.js");



const InstallButton = ({ onStartInstall }) => {
    const { loading } = (0,_contexts_packagesListContext__WEBPACK_IMPORTED_MODULE_1__.usePackageContext)();
    return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("button", { className: "mljar-packages-manager-install-button", onClick: onStartInstall, disabled: loading, title: "Install Package" },
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_icons_installPackageIcon__WEBPACK_IMPORTED_MODULE_2__.installIcon.react, { className: "mljar-packages-manager-install-icon" })));
};


/***/ }),

/***/ "./lib/components/installFrom.js":
/*!***************************************!*\
  !*** ./lib/components/installFrom.js ***!
  \***************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   InstallForm: () => (/* binding */ InstallForm)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _contexts_notebookPanelContext__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../contexts/notebookPanelContext */ "./lib/contexts/notebookPanelContext.js");
/* harmony import */ var _pcode_utils__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../pcode/utils */ "./lib/pcode/utils.js");
/* harmony import */ var _contexts_packagesListContext__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../contexts/packagesListContext */ "./lib/contexts/packagesListContext.js");




// import { infoIcon } from '../icons/infoIcon'
const isSuccess = (message) => {
    return ((message === null || message === void 0 ? void 0 : message.toLowerCase().includes('success')) ||
        (message === null || message === void 0 ? void 0 : message.toLowerCase().includes('already')) ||
        false);
};
const InstallForm = () => {
    const [packageName, setPackageName] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)('');
    const [installing, setInstalling] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)(false);
    const [message, setMessage] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)(null);
    const notebookPanel = (0,_contexts_notebookPanelContext__WEBPACK_IMPORTED_MODULE_1__.useNotebookPanelContext)();
    const { refreshPackages } = (0,_contexts_packagesListContext__WEBPACK_IMPORTED_MODULE_2__.usePackageContext)();
    const handleCheckAndInstall = () => {
        var _a, _b;
        setInstalling(true);
        setMessage(null);
        const code = (0,_pcode_utils__WEBPACK_IMPORTED_MODULE_3__.checkIfPackageInstalled)(packageName);
        const future = (_b = (_a = notebookPanel === null || notebookPanel === void 0 ? void 0 : notebookPanel.sessionContext.session) === null || _a === void 0 ? void 0 : _a.kernel) === null || _b === void 0 ? void 0 : _b.requestExecute({
            code,
            store_history: false
        });
        if (!future) {
            setInstalling(false);
            setMessage('No kernel available.');
            return;
        }
        future.onIOPub = (msg) => {
            const msgType = msg.header.msg_type;
            if (msgType === 'stream' ||
                msgType === 'execute_result' ||
                msgType === 'display_data' ||
                msgType === 'update_display_data') {
                const content = msg.content;
                if (content.text.includes('NOT_INSTALLED')) {
                    proceedWithInstall();
                }
                else if (content.text.includes('INSTALLED')) {
                    setInstalling(false);
                    setMessage('Package is already installed.');
                }
            }
            else if (msgType === 'error') {
                setInstalling(false);
                setMessage('An error occurred while checking installation. Check the correctness of the package name.');
            }
        };
    };
    const proceedWithInstall = () => {
        var _a, _b;
        const code = (0,_pcode_utils__WEBPACK_IMPORTED_MODULE_3__.installPackagePip)(packageName);
        const future = (_b = (_a = notebookPanel === null || notebookPanel === void 0 ? void 0 : notebookPanel.sessionContext.session) === null || _a === void 0 ? void 0 : _a.kernel) === null || _b === void 0 ? void 0 : _b.requestExecute({
            code,
            store_history: false
        });
        if (!future) {
            setMessage('No kernel available.');
            setInstalling(false);
            return;
        }
        future.onIOPub = (msg) => {
            const msgType = msg.header.msg_type;
            if (msgType === 'stream' ||
                msgType === 'execute_result' ||
                msgType === 'display_data' ||
                msgType === 'update_display_data') {
                const content = msg.content;
                if (content.text.includes('ERROR')) {
                    setMessage('Error installing the package.');
                    setInstalling(false);
                }
                else if (content.text.includes('Successfully installed')) {
                    setMessage('Package installed successfully.');
                    setInstalling(false);
                    refreshPackages();
                }
            }
            else if (msgType === 'error') {
                setMessage('An error occurred during installation. Check the correctness of the package name.');
                setInstalling(false);
            }
        };
    };
    return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: "mljar-packages-manager-install-form" },
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement("span", { className: "mljar-packages-manager-usage-span" },
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement("span", { style: { fontWeight: 600 } }, "Usage: "),
            "Enter",
            ' ',
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement("span", { style: { fontWeight: 600, color: '#0099cc' } }, "package_name"),
            ' ',
            "or",
            ' ',
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement("span", { style: { fontWeight: 600, color: '#0099cc' } }, "package_name==version")),
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement("input", { type: "text", value: packageName, onChange: e => setPackageName(e.target.value), placeholder: "Enter package name...", className: "mljar-packages-manager-install-input" }),
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: "mljar-packages-manager-install-form-buttons" },
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement("button", { className: "mljar-packages-manager-install-submit-button", onClick: handleCheckAndInstall, disabled: installing || packageName.trim() === '' }, installing ? 'Processing...' : 'Install')),
        message && (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("p", { className: `mljar-packages-manager-install-message ${isSuccess(message) ? 'success' : 'error'}` }, message))));
};


/***/ }),

/***/ "./lib/components/packageItem.js":
/*!***************************************!*\
  !*** ./lib/components/packageItem.js ***!
  \***************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   PackageItem: () => (/* binding */ PackageItem)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _icons_deletePackageIcon__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../icons/deletePackageIcon */ "./lib/icons/deletePackageIcon.js");
/* harmony import */ var _pcode_utils__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../pcode/utils */ "./lib/pcode/utils.js");
/* harmony import */ var _contexts_notebookPanelContext__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../contexts/notebookPanelContext */ "./lib/contexts/notebookPanelContext.js");
/* harmony import */ var _contexts_packagesListContext__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../contexts/packagesListContext */ "./lib/contexts/packagesListContext.js");
/* harmony import */ var _icons_errorIcon__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../icons/errorIcon */ "./lib/icons/errorIcon.js");
// src/components/PackageItem.tsx







const PackageItem = ({ pkg }) => {
    const notebookPanel = (0,_contexts_notebookPanelContext__WEBPACK_IMPORTED_MODULE_1__.useNotebookPanelContext)();
    const { refreshPackages } = (0,_contexts_packagesListContext__WEBPACK_IMPORTED_MODULE_2__.usePackageContext)();
    const [loading, setLoading] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)(false);
    const [error, setError] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)(false);
    const handleDelete = async () => {
        var _a, _b;
        let confirm = false;
        if (window.electron) {
            confirm = await window.electron.invoke('show-confirm-dialog', `Click "Ok" to confirm the deletion of ${pkg.name}.`);
        }
        else {
            confirm = window.confirm(`Click "Ok" to confirm the deletion of ${pkg.name}.`);
        }
        if (confirm) {
            setLoading(true);
            setError(false);
            const code = (0,_pcode_utils__WEBPACK_IMPORTED_MODULE_3__.removePackagePip)(pkg.name);
            const future = (_b = (_a = notebookPanel === null || notebookPanel === void 0 ? void 0 : notebookPanel.sessionContext.session) === null || _a === void 0 ? void 0 : _a.kernel) === null || _b === void 0 ? void 0 : _b.requestExecute({
                code,
                store_history: false
            });
            if (!future) {
                setLoading(false);
                setError(true);
                return;
            }
            future.onIOPub = (msg) => {
                const msgType = msg.header.msg_type;
                if (msgType === 'stream' ||
                    msgType === 'execute_result' ||
                    msgType === 'display_data' ||
                    msgType === 'update_display_data') {
                    const content = msg.content;
                    if (content.text.includes('ERROR')) {
                        setError(true);
                        setLoading(false);
                    }
                    else if (content.text.includes('Successfully uninstalled')) {
                        setError(false);
                        setError(false);
                        refreshPackages();
                    }
                }
                else if (msgType === 'error') {
                    setError(true);
                    setLoading(false);
                }
            };
        }
    };
    return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("li", { className: "mljar-packages-manager-list-item" },
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement("span", { className: "mljar-packages-manager-package-name" },
            " ",
            pkg.name),
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement("span", { className: "mljar-packages-manager-package-version" }, pkg.version),
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement("button", { className: "mljar-packages-manager-delete-button", onClick: handleDelete, "aria-label": error
                ? `Error during uninstalling ${pkg.name}`
                : `Uninstall ${pkg.name}`, title: `Delete ${pkg.name}` }, loading ? (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("span", { className: "mljar-packages-manager-spinner" })) : error ? (react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_icons_errorIcon__WEBPACK_IMPORTED_MODULE_4__.errorIcon.react, { className: "mljar-packages-manager-error-icon" })) : (react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_icons_deletePackageIcon__WEBPACK_IMPORTED_MODULE_5__.myDeleteIcon.react, { className: "mljar-packages-manager-delete-icon" })))));
};


/***/ }),

/***/ "./lib/components/packageList.js":
/*!***************************************!*\
  !*** ./lib/components/packageList.js ***!
  \***************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   PackageList: () => (/* binding */ PackageList)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _contexts_packagesListContext__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../contexts/packagesListContext */ "./lib/contexts/packagesListContext.js");
/* harmony import */ var _packageItem__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./packageItem */ "./lib/components/packageItem.js");
// src/components/PackageList.tsx



const PackageList = () => {
    const { packages, searchTerm } = (0,_contexts_packagesListContext__WEBPACK_IMPORTED_MODULE_1__.usePackageContext)();
    const filteredPackages = packages.filter(pkg => pkg.name.toLowerCase().includes(searchTerm.toLowerCase()));
    if (filteredPackages.length === 0) {
        return react__WEBPACK_IMPORTED_MODULE_0___default().createElement("p", null, "Sorry, no packages found or notebook is closed.");
    }
    return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("ul", { className: "mljar-packages-manager-list" },
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement("li", { className: "mljar-packages-manager-list-header" },
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement("span", { className: "mljar-packages-manager-header-name" }, "Name"),
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement("span", { className: "mljar-packages-manager-header-version" }, "Version"),
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement("span", { className: "mljar-packages-manager-header-blank" }, "\u00A0")),
        filteredPackages
            .sort((a, b) => a.name.localeCompare(b.name))
            .map(pkg => (react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_packageItem__WEBPACK_IMPORTED_MODULE_2__.PackageItem, { key: pkg.name, pkg: pkg })))));
};


/***/ }),

/***/ "./lib/components/packageListComponent.js":
/*!************************************************!*\
  !*** ./lib/components/packageListComponent.js ***!
  \************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   PackageListComponent: () => (/* binding */ PackageListComponent)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _components_searchBar__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../components/searchBar */ "./lib/components/searchBar.js");
/* harmony import */ var _components_packageListContent__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ../components/packageListContent */ "./lib/components/packageListContent.js");
/* harmony import */ var _contexts_packagesListContext__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../contexts/packagesListContext */ "./lib/contexts/packagesListContext.js");
/* harmony import */ var _components_refreshButton__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../components/refreshButton */ "./lib/components/refreshButton.js");
/* harmony import */ var _components_installButton__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../components/installButton */ "./lib/components/installButton.js");
/* harmony import */ var _components_backButton__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../components/backButton */ "./lib/components/backButton.js");
/* harmony import */ var _installFrom__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ./installFrom */ "./lib/components/installFrom.js");
// src/components/PackageListComponent.tsx








const PackageListComponent = () => {
    const [view, setView] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)('list');
    const handleStartInstall = () => {
        setView('install');
    };
    const handleBack = () => {
        setView('list');
    };
    return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_contexts_packagesListContext__WEBPACK_IMPORTED_MODULE_1__.PackageContextProvider, null,
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: "mljar-packages-manager-container" },
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: "mljar-packages-manager-header-container" },
                view === 'list' && (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("h3", { className: "mljar-packages-manager-header" }, "Packages Manager")),
                view === 'install' && (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("h3", { className: "mljar-packages-manager-header" }, "Install Packages")),
                view === 'list' && react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_components_refreshButton__WEBPACK_IMPORTED_MODULE_2__.RefreshButton, null),
                view === 'list' && (react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_components_installButton__WEBPACK_IMPORTED_MODULE_3__.InstallButton, { onStartInstall: handleStartInstall })),
                view === 'install' && react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_components_backButton__WEBPACK_IMPORTED_MODULE_4__.BackButton, { onBack: handleBack })),
            view === 'list' ? (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", null,
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_components_searchBar__WEBPACK_IMPORTED_MODULE_5__.SearchBar, null),
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_components_packageListContent__WEBPACK_IMPORTED_MODULE_6__.PackageListContent, null))) : (react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_installFrom__WEBPACK_IMPORTED_MODULE_7__.InstallForm, null)))));
};


/***/ }),

/***/ "./lib/components/packageListContent.js":
/*!**********************************************!*\
  !*** ./lib/components/packageListContent.js ***!
  \**********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   PackageListContent: () => (/* binding */ PackageListContent)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _contexts_packagesListContext__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../contexts/packagesListContext */ "./lib/contexts/packagesListContext.js");
/* harmony import */ var _components_packageList__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../components/packageList */ "./lib/components/packageList.js");



const PackageListContent = () => {
    const { loading, error } = (0,_contexts_packagesListContext__WEBPACK_IMPORTED_MODULE_1__.usePackageContext)();
    return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: "mljar-packages-manager-list-container" },
        loading && (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: "mljar-packages-manager-spinner-container" },
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: "mljar-packages-manager-spinner", role: "status", "aria-label": "Loading" }))),
        error && react__WEBPACK_IMPORTED_MODULE_0___default().createElement("p", { className: "mljar-packages-manager-error-message" }, error),
        !loading && !error && react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_components_packageList__WEBPACK_IMPORTED_MODULE_2__.PackageList, null)));
};


/***/ }),

/***/ "./lib/components/refreshButton.js":
/*!*****************************************!*\
  !*** ./lib/components/refreshButton.js ***!
  \*****************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   RefreshButton: () => (/* binding */ RefreshButton)
/* harmony export */ });
/* harmony import */ var _contexts_packagesListContext__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../contexts/packagesListContext */ "./lib/contexts/packagesListContext.js");
/* harmony import */ var _icons_refreshIcon__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../icons/refreshIcon */ "./lib/icons/refreshIcon.js");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);



const RefreshButton = () => {
    const { refreshPackages, loading } = (0,_contexts_packagesListContext__WEBPACK_IMPORTED_MODULE_1__.usePackageContext)();
    return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("button", { className: "mljar-packages-manager-refresh-button", onClick: refreshPackages, disabled: loading, title: "Refresh Packages" },
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_icons_refreshIcon__WEBPACK_IMPORTED_MODULE_2__.refreshIcon.react, { className: "mljar-packages-manager-refresh-icon" })));
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
/* harmony import */ var _contexts_packagesListContext__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../contexts/packagesListContext */ "./lib/contexts/packagesListContext.js");
// src/components/SearchBar.tsx


const SearchBar = () => {
    const { searchTerm, setSearchTerm } = (0,_contexts_packagesListContext__WEBPACK_IMPORTED_MODULE_1__.usePackageContext)();
    const handleChange = (e) => {
        setSearchTerm(e.target.value);
    };
    return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: "mljar-packages-manager-search-bar-container" },
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement("input", { type: "text", value: searchTerm, onChange: handleChange, placeholder: "Search Package...", className: 'mljar-packages-manager-search-bar-input' })));
};


/***/ }),

/***/ "./lib/contexts/notebookKernelContext.js":
/*!***********************************************!*\
  !*** ./lib/contexts/notebookKernelContext.js ***!
  \***********************************************/
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

/***/ "./lib/contexts/notebookPanelContext.js":
/*!**********************************************!*\
  !*** ./lib/contexts/notebookPanelContext.js ***!
  \**********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   NotebookPanelContextProvider: () => (/* binding */ NotebookPanelContextProvider),
/* harmony export */   useNotebookPanelContext: () => (/* binding */ useNotebookPanelContext)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
// contexts/notebook-panel-context.tsx

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

/***/ "./lib/contexts/packagesListContext.js":
/*!*********************************************!*\
  !*** ./lib/contexts/packagesListContext.js ***!
  \*********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   PackageContextProvider: () => (/* binding */ PackageContextProvider),
/* harmony export */   usePackageContext: () => (/* binding */ usePackageContext)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _notebookPanelContext__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./notebookPanelContext */ "./lib/contexts/notebookPanelContext.js");
/* harmony import */ var _notebookKernelContext__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./notebookKernelContext */ "./lib/contexts/notebookKernelContext.js");
/* harmony import */ var _pcode_utils__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../pcode/utils */ "./lib/pcode/utils.js");
// src/contexts/PackageContext.tsx




const PackageContext = (0,react__WEBPACK_IMPORTED_MODULE_0__.createContext)(undefined);
let kernelIdToPackagesList = {};
const PackageContextProvider = ({ children }) => {
    const notebookPanel = (0,_notebookPanelContext__WEBPACK_IMPORTED_MODULE_1__.useNotebookPanelContext)();
    const kernel = (0,_notebookKernelContext__WEBPACK_IMPORTED_MODULE_2__.useNotebookKernelContext)();
    const [packages, setPackages] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)([]);
    const [loading, setLoading] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)(false);
    const [error, setError] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)(null);
    const [searchTerm, setSearchTerm] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)('');
    const executeCode = (0,react__WEBPACK_IMPORTED_MODULE_0__.useCallback)(async () => {
        var _a, _b, _c, _d, _e, _f;
        setPackages([]);
        setLoading(true);
        setError(null);
        if (!notebookPanel || !kernel) {
            setLoading(false);
            return;
        }
        try {
            const kernelId = (_c = (_b = (_a = notebookPanel.sessionContext) === null || _a === void 0 ? void 0 : _a.session) === null || _b === void 0 ? void 0 : _b.kernel) === null || _c === void 0 ? void 0 : _c.id;
            // check if there are packages for current kernel, if yes load them
            // otherwise run code request to Python kernel
            if (kernelId !== undefined &&
                kernelId !== null &&
                kernelId in kernelIdToPackagesList) {
                setPackages(kernelIdToPackagesList[kernelId]);
                setLoading(false);
            }
            else {
                const future = (_f = (_e = (_d = notebookPanel.sessionContext) === null || _d === void 0 ? void 0 : _d.session) === null || _e === void 0 ? void 0 : _e.kernel) === null || _f === void 0 ? void 0 : _f.requestExecute({
                    code: _pcode_utils__WEBPACK_IMPORTED_MODULE_3__.listPackagesCode,
                    store_history: false
                });
                if (future) {
                    future.onIOPub = (msg) => {
                        const msgType = msg.header.msg_type;
                        if (msgType === 'execute_result' ||
                            msgType === 'display_data' ||
                            msgType === 'update_display_data') {
                            const content = msg.content;
                            const jsonData = content.data['application/json'];
                            const textData = content.data['text/plain'];
                            if (jsonData) {
                                if (Array.isArray(jsonData)) {
                                    setPackages(jsonData);
                                }
                                else {
                                    console.warn('Data is not JSON:', jsonData);
                                }
                                setLoading(false);
                            }
                            else if (textData) {
                                try {
                                    const cleanedData = textData.replace(/^['"]|['"]$/g, '');
                                    const doubleQuotedData = cleanedData.replace(/'/g, '"');
                                    const parsedData = JSON.parse(doubleQuotedData);
                                    if (Array.isArray(parsedData)) {
                                        setPackages([]);
                                        setPackages(parsedData);
                                        if (kernelId !== undefined && kernelId !== null) {
                                            kernelIdToPackagesList[kernelId] = parsedData;
                                        }
                                    }
                                    else {
                                        throw new Error('Error during parsing.');
                                    }
                                    setLoading(false);
                                }
                                catch (err) {
                                    console.error('Error during export JSON from text/plain:', err);
                                    setError('Error during export JSON');
                                    setLoading(false);
                                }
                            }
                        }
                    };
                }
            }
        }
        catch (err) {
            console.error('Unexpected error:', err);
            setError('Unexpected error');
            setLoading(false);
        }
    }, [notebookPanel, kernel]);
    (0,react__WEBPACK_IMPORTED_MODULE_0__.useEffect)(() => {
        executeCode();
    }, [executeCode]);
    return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement(PackageContext.Provider, { value: {
            packages,
            loading,
            error,
            searchTerm,
            setSearchTerm,
            refreshPackages: () => {
                // clear all stored packages for all kernels
                kernelIdToPackagesList = {};
                executeCode();
            }
        } }, children));
};
const usePackageContext = () => {
    const context = (0,react__WEBPACK_IMPORTED_MODULE_0__.useContext)(PackageContext);
    if (context === undefined) {
        throw new Error('usePackageContext must be used within a PackageProvider');
    }
    return context;
};


/***/ }),

/***/ "./lib/icons/backIcon.js":
/*!*******************************!*\
  !*** ./lib/icons/backIcon.js ***!
  \*******************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   backIcon: () => (/* binding */ backIcon)
/* harmony export */ });
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__);

const svgStr = `
<svg  xmlns="http://www.w3.org/2000/svg"  width="24"  height="24"  viewBox="0 0 24 24"  fill="none"  stroke="currentColor"  stroke-width="2"  stroke-linecap="round"  stroke-linejoin="round"  class="icon icon-tabler icons-tabler-outline icon-tabler-arrow-back-up"><path stroke="none" d="M0 0h24v24H0z" fill="none"/><path d="M9 14l-4 -4l4 -4" /><path d="M5 10h11a4 4 0 1 1 0 8h-1" /></svg>
`;
const backIcon = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.LabIcon({
    name: 'my-back-icon',
    svgstr: svgStr,
});


/***/ }),

/***/ "./lib/icons/deletePackageIcon.js":
/*!****************************************!*\
  !*** ./lib/icons/deletePackageIcon.js ***!
  \****************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   myDeleteIcon: () => (/* binding */ myDeleteIcon)
/* harmony export */ });
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__);

const svgStr = `
<svg  xmlns="http://www.w3.org/2000/svg"  width="24"  height="24"  viewBox="0 0 24 24"  fill="none"  stroke="currentColor"  stroke-width="2"  stroke-linecap="round"  stroke-linejoin="round"  class="icon icon-tabler icons-tabler-outline icon-tabler-trash"><path stroke="none" d="M0 0h24v24H0z" fill="none"/><path d="M4 7l16 0" /><path d="M10 11l0 6" /><path d="M14 11l0 6" /><path d="M5 7l1 12a2 2 0 0 0 2 2h8a2 2 0 0 0 2 -2l1 -12" /><path d="M9 7v-3a1 1 0 0 1 1 -1h4a1 1 0 0 1 1 1v3" /></svg>
`;
const myDeleteIcon = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.LabIcon({
    name: 'my-delete-icon',
    svgstr: svgStr,
});


/***/ }),

/***/ "./lib/icons/errorIcon.js":
/*!********************************!*\
  !*** ./lib/icons/errorIcon.js ***!
  \********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   errorIcon: () => (/* binding */ errorIcon)
/* harmony export */ });
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__);

const svgStr = `
<svg  xmlns="http://www.w3.org/2000/svg"  width="24"  height="24"  viewBox="0 0 24 24"  fill="none"  stroke="currentColor"  stroke-width="2"  stroke-linecap="round"  stroke-linejoin="round"  class="icon icon-tabler icons-tabler-outline icon-tabler-zoom-exclamation"><path stroke="none" d="M0 0h24v24H0z" fill="none"/><path d="M10 10m-7 0a7 7 0 1 0 14 0a7 7 0 1 0 -14 0" /><path d="M21 21l-6 -6" /><path d="M10 13v.01" /><path d="M10 7v3" /></svg>
`;
const errorIcon = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.LabIcon({
    name: 'my-error-icon',
    svgstr: svgStr,
});


/***/ }),

/***/ "./lib/icons/installPackageIcon.js":
/*!*****************************************!*\
  !*** ./lib/icons/installPackageIcon.js ***!
  \*****************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   installIcon: () => (/* binding */ installIcon)
/* harmony export */ });
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__);

const svgStr = `
<svg  xmlns="http://www.w3.org/2000/svg"  width="24"  height="24"  viewBox="0 0 24 24"  fill="none"  stroke="currentColor"  stroke-width="2"  stroke-linecap="round"  stroke-linejoin="round"  class="icon icon-tabler icons-tabler-outline icon-tabler-cube-plus"><path stroke="none" d="M0 0h24v24H0z" fill="none"/><path d="M21 12.5v-4.509a1.98 1.98 0 0 0 -1 -1.717l-7 -4.008a2.016 2.016 0 0 0 -2 0l-7 4.007c-.619 .355 -1 1.01 -1 1.718v8.018c0 .709 .381 1.363 1 1.717l7 4.008a2.016 2.016 0 0 0 2 0" /><path d="M12 22v-10" /><path d="M12 12l8.73 -5.04" /><path d="M3.27 6.96l8.73 5.04" /><path d="M16 19h6" /><path d="M19 16v6" /></svg>
`;
const installIcon = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.LabIcon({
    name: 'my-install-icon',
    svgstr: svgStr,
});


/***/ }),

/***/ "./lib/icons/packageManagerIcon.js":
/*!*****************************************!*\
  !*** ./lib/icons/packageManagerIcon.js ***!
  \*****************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   packageManagerIcon: () => (/* binding */ packageManagerIcon)
/* harmony export */ });
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__);

const svgStr = `
<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="icon icon-tabler icons-tabler-outline icon-tabler-package-export">
  <path stroke="none" d="M0 0h24v24H0z" fill="none"/>
  <path d="M12 21l-8 -4.5v-9l8 -4.5l8 4.5v4.5" />
  <path d="M12 12l8 -4.5" />
  <path d="M12 12v9" />
  <path d="M12 12l-8 -4.5" />
  <path d="M15 18h7" />
  <path d="M19 15l3 3l-3 3" />
</svg>
`;
const packageManagerIcon = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.LabIcon({
    name: 'package-manager-icon',
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
    name: 'my-refresh-icon',
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
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _packageManagerSidebar__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./packageManagerSidebar */ "./lib/packageManagerSidebar.js");
/* harmony import */ var _watchers_notebookWatcher__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./watchers/notebookWatcher */ "./lib/watchers/notebookWatcher.js");


const leftTab = {
    id: 'package-manager:plugin',
    description: 'A JupyterLab extension to list, remove and install python packages from pip.',
    autoStart: true,
    activate: async (app) => {
        const notebookWatcher = new _watchers_notebookWatcher__WEBPACK_IMPORTED_MODULE_0__.NotebookWatcher(app.shell);
        notebookWatcher.selectionChanged.connect((sender, selections) => { });
        const widget = (0,_packageManagerSidebar__WEBPACK_IMPORTED_MODULE_1__.createPackageManagerSidebar)(notebookWatcher);
        app.shell.add(widget, 'left', { rank: 1999 });
    }
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (leftTab);


/***/ }),

/***/ "./lib/packageManagerSidebar.js":
/*!**************************************!*\
  !*** ./lib/packageManagerSidebar.js ***!
  \**************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   createPackageManagerSidebar: () => (/* binding */ createPackageManagerSidebar)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _icons_packageManagerIcon__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./icons/packageManagerIcon */ "./lib/icons/packageManagerIcon.js");
/* harmony import */ var _contexts_notebookPanelContext__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./contexts/notebookPanelContext */ "./lib/contexts/notebookPanelContext.js");
/* harmony import */ var _contexts_notebookKernelContext__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./contexts/notebookKernelContext */ "./lib/contexts/notebookKernelContext.js");
/* harmony import */ var _components_packageListComponent__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./components/packageListComponent */ "./lib/components/packageListComponent.js");






class PackageManagerSidebarWidget extends _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__.ReactWidget {
    constructor(notebookWatcher) {
        super();
        this.notebookWatcher = notebookWatcher;
        this.id = 'package-manager::empty-sidebar';
        this.title.icon = _icons_packageManagerIcon__WEBPACK_IMPORTED_MODULE_2__.packageManagerIcon;
        this.title.caption = 'Package Manager';
        this.addClass('mljar-packages-manager-sidebar-widget');
    }
    render() {
        return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: 'mljar-packages-manager-sidebar-container' },
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_contexts_notebookPanelContext__WEBPACK_IMPORTED_MODULE_3__.NotebookPanelContextProvider, { notebookWatcher: this.notebookWatcher },
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_contexts_notebookKernelContext__WEBPACK_IMPORTED_MODULE_4__.NotebookKernelContextProvider, { notebookWatcher: this.notebookWatcher },
                    react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_components_packageListComponent__WEBPACK_IMPORTED_MODULE_5__.PackageListComponent, null)))));
    }
}
function createPackageManagerSidebar(notebookWatcher) {
    return new PackageManagerSidebarWidget(notebookWatcher);
}


/***/ }),

/***/ "./lib/pcode/utils.js":
/*!****************************!*\
  !*** ./lib/pcode/utils.js ***!
  \****************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   checkIfPackageInstalled: () => (/* binding */ checkIfPackageInstalled),
/* harmony export */   installPackagePip: () => (/* binding */ installPackagePip),
/* harmony export */   listPackagesCode: () => (/* binding */ listPackagesCode),
/* harmony export */   removePackagePip: () => (/* binding */ removePackagePip)
/* harmony export */ });
const listPackagesCode = `
def __mljar__list_packages():
    from importlib.metadata import distributions
    pkgs = []
    seen = set()
    for dist in distributions():
        name = dist.metadata["Name"]
        if name not in seen:
            seen.add(name)
            pkgs.append({"name": name, "version": dist.version})
    return pkgs

__mljar__list_packages()
`;
const installPackagePip = (pkg) => `
def __mljar__install_pip():
    import subprocess
    import sys
    python_exe = sys.executable
    if python_exe.startswith('\\\\?'):
        python_exe = python_exe[4:] 
    subprocess.check_call([python_exe, '-m', 'pip', 'install', '${pkg}'])
__mljar__install_pip()
`;
const removePackagePip = (pkg) => `
def __mljar__remove_package():
    import subprocess
    import sys
    python_exe = sys.executable
    if python_exe.startswith('\\\\?'):
        python_exe = python_exe[4:]
    subprocess.check_call([python_exe, '-m', 'pip', 'uninstall', '-y', '${pkg}'])
__mljar__remove_package()
`;
const checkIfPackageInstalled = (pkg) => `
def __mljar__check_if_installed():
    from importlib.metadata import distributions
    for dist in distributions():
        if dist.metadata["Name"].lower() == "${pkg}".lower():
            print("INSTALLED")
            return
    print("NOT_INSTALLED")
__mljar__check_if_installed()
`;


/***/ }),

/***/ "./lib/watchers/notebookWatcher.js":
/*!*****************************************!*\
  !*** ./lib/watchers/notebookWatcher.js ***!
  \*****************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   NotebookWatcher: () => (/* binding */ NotebookWatcher),
/* harmony export */   getNotebookSelections: () => (/* binding */ getNotebookSelections)
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
function getNotebookSelections(notebook) {
    var _a;
    const selections = [];
    const cellModels = (_a = notebook.model) === null || _a === void 0 ? void 0 : _a.cells;
    if (cellModels) {
        for (let i = 0; i < cellModels.length; i++) {
            const cell = cellModels.get(i);
            const cellSource = cell === null || cell === void 0 ? void 0 : cell.sharedModel.getSource();
            const cellId = cell === null || cell === void 0 ? void 0 : cell.id;
            if (cellSource && cellId) {
                const numLines = cellSource.split('\n').length;
                const selection = {
                    start: { line: 0, column: 0 },
                    end: { line: numLines - 1, column: cellSource.length },
                    text: cellSource,
                    numLines,
                    widgetId: notebook.id,
                    cellId
                };
                selections.push(selection);
            }
        }
    }
    return selections;
}
class NotebookWatcher {
    constructor(shell) {
        var _a;
        this._kernelInfo = null;
        this._kernelChanged = new _lumino_signaling__WEBPACK_IMPORTED_MODULE_1__.Signal(this);
        this._mainAreaWidget = null;
        this._selections = [];
        this._selectionChanged = new _lumino_signaling__WEBPACK_IMPORTED_MODULE_1__.Signal(this);
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
    get selection() {
        return this._selections;
    }
    get selectionChanged() {
        return this._selectionChanged;
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
    // protected _poll(): void {
    //   const notebook = getNotebook(this._mainAreaWidget);
    //   const currSelections = notebook ? getNotebookSelections(notebook) : [];
    //
    //   if (JSON.stringify(this._selections) === JSON.stringify(currSelections)) {
    //     return;
    //   }
    //
    //   this._selections = currSelections;
    //   this._selectionChanged.emit(currSelections);
    //
    //   const newNotebookPanel = this.notebookPanel();
    //   if (this._notebookPanel !== newNotebookPanel) {
    //     this._notebookPanel = newNotebookPanel;
    //     this._notebookPanelChanged.emit(this._notebookPanel);
    //   }
    // }
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
//# sourceMappingURL=lib_index_js.df5a79c1e886b99c3f8a.js.map