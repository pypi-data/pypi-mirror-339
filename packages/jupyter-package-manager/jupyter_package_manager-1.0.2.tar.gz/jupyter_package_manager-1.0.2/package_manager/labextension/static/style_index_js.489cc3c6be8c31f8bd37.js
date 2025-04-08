"use strict";
(self["webpackChunkjupyter_package_manager"] = self["webpackChunkjupyter_package_manager"] || []).push([["style_index_js"],{

/***/ "./node_modules/css-loader/dist/cjs.js!./style/base.css":
/*!**************************************************************!*\
  !*** ./node_modules/css-loader/dist/cjs.js!./style/base.css ***!
  \**************************************************************/
/***/ ((module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _node_modules_css_loader_dist_runtime_sourceMaps_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../node_modules/css-loader/dist/runtime/sourceMaps.js */ "./node_modules/css-loader/dist/runtime/sourceMaps.js");
/* harmony import */ var _node_modules_css_loader_dist_runtime_sourceMaps_js__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_node_modules_css_loader_dist_runtime_sourceMaps_js__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../node_modules/css-loader/dist/runtime/api.js */ "./node_modules/css-loader/dist/runtime/api.js");
/* harmony import */ var _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1__);
// Imports


var ___CSS_LOADER_EXPORT___ = _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1___default()((_node_modules_css_loader_dist_runtime_sourceMaps_js__WEBPACK_IMPORTED_MODULE_0___default()));
// Module
___CSS_LOADER_EXPORT___.push([module.id, `.mljar-packages-manager-sidebar-container {
  display: flex;
  flex-direction: column;
  height: 100%;
  overflow-y: auto;
}

.mljar-packages-manager-search-bar-container {
  margin: 0px 10px 10px 0px;
}
.mljar-packages-manager-install-input,
.mljar-packages-manager-search-bar-input {
  width: 100%;
  padding: 8px;
  box-sizing: border-box;
  background-color: var(--jp-layout-color1);
  color: var(--jp-ui-font-color1);
  border: 1px solid var(--jp-border-color2);
  border-radius: 5px;
}

.mljar-packages-manager-install-input {
  margin-bottom: 8px;
}

.mljar-packages-manager-install-input:focus,
.mljar-packages-manager-search-bar-input:focus {
  outline: none;
  border: 2px solid var(--jp-ui-font-color1);
}
.mljar-packages-manager-install-input::placeholder,
.mljar-packages-manager-search-bar-input::placeholder {
  color: var(--jp-ui-font-color2);
}

.mljar-packages-manager-container {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.mljar-packages-manager-header-container {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  margin-bottom: 8px;
  margin-right: 8px;
  border-bottom: 2px solid #ddd;
}

.mljar-packages-manager-header {
  flex: 4;
  font-size: 0.85rem;
  font-weight: 700;
  color: var(--jp-ui-font-color1);
  text-align: left;
  padding-bottom: 8px;
  margin: 0;
}

.mljar-packages-manager-list-container {
  flex: 1;
  overflow-y: hidden;
  padding-right: 10px;
}

.mljar-packages-manager-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.mljar-packages-manager-list-container::-webkit-scrollbar {
  width: 8px;
}

.mljar-packages-manager-list-container::-webkit-scrollbar-thumb {
  background-color: rgba(0, 0, 0, 0.2);
  border-radius: 4px;
}

.mljar-packages-manager-list-container::-webkit-scrollbar-track {
  background-color: rgba(0, 0, 0, 0.05);
}

.mljar-packages-manager-sidebar-widget {
  background-color: #ffffff;
  padding: 10px;
  font-family: 'Courier New', Courier, monospace;
}

.mljar-packages-manager-back-button,
.mljar-packages-manager-install-button,
.mljar-packages-manager-refresh-button {
  width: 30px;
  display: flex;
  margin: 1px 0px 2px 0px;
  align-items: center;
  justify-content: center;
  gap: 8px;
  color: #0099cc;
  border: none;
  border-radius: 4px;
  padding: 8px 0px;
  cursor: pointer;
  font-size: 0.75rem;
  transition: background-color 0.3s ease;
}

.mljar-packages-manager-back-button {
  width: 70px !important;
  text-align: center;
  padding-right: 4px;
}

.mljar-packages-manager-back-button:hover:not(:disabled),
.mljar-packages-manager-refresh-button:hover:not(:disabled),
.mljar-packages-manager-install-button:hover:not(:disabled) {
  background-color: #0099cc;
  color: #ffffff;
}

.mljar-packages-manager-delete-button {
  visibility: hidden;
  background: none;
  position: relative;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  padding: 4px;
  margin: 5px auto;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #dc3545;
  transition: background-color 0.3s ease;
}

.mljar-packages-manager-refresh-button:disabled,
.mljar-packages-manager-install-button:disabled,
.mljar-packages-manager-back-button:disabled {
  cursor: not-allowed;
}

.mljar-packages-manager-install-submit-button {
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #28a745;
  color: white;
  border: none;
  border-radius: 4px;
  padding: 8px 12px;
  cursor: pointer;
  font-size: 0.75rem;
  transition: background-color 0.3s ease;
}

.mljar-packages-manager-install-submit-button:disabled {
  background-color: #94d3a2;
  cursor: not-allowed;
}

.mljar-packages-manager-install-submit-button:hover:not(:disabled) {
  background-color: #1e7e34;
}

.mljar-packages-manager-delete-button:hover {
  color: #fff;
  background-color: #dc3545;
  transition: background-color 0.3s ease;
}

.mljar-packages-manager-list-item:hover .mljar-packages-manager-delete-button {
  visibility: visible;
}

.mljar-packages-manager-refresh-icon,
.mljar-packages-manager-install-icon,
.mljar-packages-manager-back-icon {
  display: flex;
  align-items: center;
  width: 15px;
  height: 15px;
}

.mljar-packages-manager-delete-icon {
  display: flex;
  align-items: center;
  width: 20px;
  height: 20px;
}

.mljar-packages-manager-error-icon {
  color: #dc3545;
  width: 15px;
  height: 15px;
}

.mljar-packages-manager-info-icon-container {
  position: relative;
  display: inline-block;
  cursor: pointer;
}

.mljar-packages-manager-info-icon-container span:first-child {
  display: inline-flex;
  align-items: center;
  color: #0099cc;
  margin: 0px;
  width: 18px;
  height: 18px;
}

.mljar-packages-manager-info-icon-container {
  visibility: hidden;
  width: 150px;
  background-color: #28a745;
  color: white;
  text-align: center;
  border-radius: 4px;
  padding: 5px;
  position: absolute;
  left: -160px;
  top: 100%;
  z-index: 1;
  opacity: 0;
  transition: opacity 0.3s;
  white-space: pre-line;
}

.mljar-packages-manager-info-icon-container:hover {
  visibility: visible;
  opacity: 1;
}

.mljar-packages-manager-install-form {
  display: flex;
  flex-direction: column;
  margin-right: 8px;
}

.mljar-packages-manager-install-form h4 {
  margin-top: 0px;
  margin-bottom: 4px;
  padding: 0;
}

.mljar-packages-manager-usage-span {
  margin-bottom: 8px;
  text-align: left;
  font-size: 0.8rem;
  padding: 5px 2px;
}

.mljar-packages-manager-install-message {
  color: #28a745;
  font-weight: bold;
  margin-top: 10px;
  text-align: left;
  padding: 5px 2px;
}

.mljar-packages-manager-install-message.error {
  color: #dc3545;
}

.mljar-packages-manager-error-message {
  color: #dc3545;
  font-weight: bold;
}

.mljar-packages-manager-spinner-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
  padding: 20px;
}

.mljar-packages-manager-spinner {
  border: 4px solid rgba(0, 0, 0, 0.1);
  width: 10px;
  height: 10px;
  border-radius: 50%;
  border-left-color: #ffffff;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.mljar-packages-manager-list-item {
  flex: 1;
  display: grid;
  grid-template-columns: 1fr 1fr 2rem;
  align-items: center;
  min-height: 38px;
  column-gap: 1rem;
  padding-left: 8px;
  padding-right: 8px;
  border-bottom: 1px solid var(--jp-border-color2);
  border-left: 1px solid var(--jp-border-color2);
  border-right: 1px solid var(--jp-border-color2);
  margin-bottom: 0px;
  margin-right: 0px;
  width: 100%;
  box-sizing: border-box;
  background-color: var(--jp-layout-color0);
  font-size: 0.7rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.mljar-packages-manager-list-item:hover {
  background-color: var(--jp-layout-color2);
  cursor: pointer;
}

.mljar-packages-manager-list-item.active {
  background-color: var(--jp-brand-color1);
  color: var(--jp-ui-inverse-font-color1);
}

.mljar-packages-manager-package-name,
.mljar-packages-manager-package-version {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.mljar-packages-manager-package-name {
  font-weight: 600;
}

.mljar-packages-manager-list-header {
  display: grid;
  grid-template-columns: 1fr 1fr 2rem;
  align-items: center;
  font-size: 0.85rem;
  padding-left: 8px;
  padding-right: 8px;
  padding-top: 10px;
  padding-bottom: 10px;
  background-color: var(--jp-layout-color0);
  color: #0099cc;
  border: 1px solid #0099cc;
  border-top-right-radius: 5px;
  border-top-left-radius: 5px;
  font-weight: 800;
}

.mljar-packages-manager-sidebar-container::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

.mljar-packages-manager-sidebar-container::-webkit-scrollbar-track {
  background: #d3d3d3;
  border-radius: 8px;
}

.mljar-packages-manager-sidebar-container::-webkit-scrollbar-thumb {
  background-color: rgba(255, 255, 255, 0.6);
  border-radius: 8px;
  border: 2px solid transparent;
  background-clip: padding-box;
}
`, "",{"version":3,"sources":["webpack://./style/base.css"],"names":[],"mappings":"AAAA;EACE,aAAa;EACb,sBAAsB;EACtB,YAAY;EACZ,gBAAgB;AAClB;;AAEA;EACE,yBAAyB;AAC3B;AACA;;EAEE,WAAW;EACX,YAAY;EACZ,sBAAsB;EACtB,yCAAyC;EACzC,+BAA+B;EAC/B,yCAAyC;EACzC,kBAAkB;AACpB;;AAEA;EACE,kBAAkB;AACpB;;AAEA;;EAEE,aAAa;EACb,0CAA0C;AAC5C;AACA;;EAEE,+BAA+B;AACjC;;AAEA;EACE,aAAa;EACb,sBAAsB;EACtB,YAAY;AACd;;AAEA;EACE,aAAa;EACb,8BAA8B;EAC9B,qBAAqB;EACrB,kBAAkB;EAClB,iBAAiB;EACjB,6BAA6B;AAC/B;;AAEA;EACE,OAAO;EACP,kBAAkB;EAClB,gBAAgB;EAChB,+BAA+B;EAC/B,gBAAgB;EAChB,mBAAmB;EACnB,SAAS;AACX;;AAEA;EACE,OAAO;EACP,kBAAkB;EAClB,mBAAmB;AACrB;;AAEA;EACE,gBAAgB;EAChB,UAAU;EACV,SAAS;AACX;;AAEA;EACE,UAAU;AACZ;;AAEA;EACE,oCAAoC;EACpC,kBAAkB;AACpB;;AAEA;EACE,qCAAqC;AACvC;;AAEA;EACE,yBAAyB;EACzB,aAAa;EACb,8CAA8C;AAChD;;AAEA;;;EAGE,WAAW;EACX,aAAa;EACb,uBAAuB;EACvB,mBAAmB;EACnB,uBAAuB;EACvB,QAAQ;EACR,cAAc;EACd,YAAY;EACZ,kBAAkB;EAClB,gBAAgB;EAChB,eAAe;EACf,kBAAkB;EAClB,sCAAsC;AACxC;;AAEA;EACE,sBAAsB;EACtB,kBAAkB;EAClB,kBAAkB;AACpB;;AAEA;;;EAGE,yBAAyB;EACzB,cAAc;AAChB;;AAEA;EACE,kBAAkB;EAClB,gBAAgB;EAChB,kBAAkB;EAClB,YAAY;EACZ,kBAAkB;EAClB,eAAe;EACf,YAAY;EACZ,gBAAgB;EAChB,aAAa;EACb,mBAAmB;EACnB,uBAAuB;EACvB,cAAc;EACd,sCAAsC;AACxC;;AAEA;;;EAGE,mBAAmB;AACrB;;AAEA;EACE,aAAa;EACb,mBAAmB;EACnB,uBAAuB;EACvB,yBAAyB;EACzB,YAAY;EACZ,YAAY;EACZ,kBAAkB;EAClB,iBAAiB;EACjB,eAAe;EACf,kBAAkB;EAClB,sCAAsC;AACxC;;AAEA;EACE,yBAAyB;EACzB,mBAAmB;AACrB;;AAEA;EACE,yBAAyB;AAC3B;;AAEA;EACE,WAAW;EACX,yBAAyB;EACzB,sCAAsC;AACxC;;AAEA;EACE,mBAAmB;AACrB;;AAEA;;;EAGE,aAAa;EACb,mBAAmB;EACnB,WAAW;EACX,YAAY;AACd;;AAEA;EACE,aAAa;EACb,mBAAmB;EACnB,WAAW;EACX,YAAY;AACd;;AAEA;EACE,cAAc;EACd,WAAW;EACX,YAAY;AACd;;AAEA;EACE,kBAAkB;EAClB,qBAAqB;EACrB,eAAe;AACjB;;AAEA;EACE,oBAAoB;EACpB,mBAAmB;EACnB,cAAc;EACd,WAAW;EACX,WAAW;EACX,YAAY;AACd;;AAEA;EACE,kBAAkB;EAClB,YAAY;EACZ,yBAAyB;EACzB,YAAY;EACZ,kBAAkB;EAClB,kBAAkB;EAClB,YAAY;EACZ,kBAAkB;EAClB,YAAY;EACZ,SAAS;EACT,UAAU;EACV,UAAU;EACV,wBAAwB;EACxB,qBAAqB;AACvB;;AAEA;EACE,mBAAmB;EACnB,UAAU;AACZ;;AAEA;EACE,aAAa;EACb,sBAAsB;EACtB,iBAAiB;AACnB;;AAEA;EACE,eAAe;EACf,kBAAkB;EAClB,UAAU;AACZ;;AAEA;EACE,kBAAkB;EAClB,gBAAgB;EAChB,iBAAiB;EACjB,gBAAgB;AAClB;;AAEA;EACE,cAAc;EACd,iBAAiB;EACjB,gBAAgB;EAChB,gBAAgB;EAChB,gBAAgB;AAClB;;AAEA;EACE,cAAc;AAChB;;AAEA;EACE,cAAc;EACd,iBAAiB;AACnB;;AAEA;EACE,aAAa;EACb,uBAAuB;EACvB,mBAAmB;EACnB,YAAY;EACZ,aAAa;AACf;;AAEA;EACE,oCAAoC;EACpC,WAAW;EACX,YAAY;EACZ,kBAAkB;EAClB,0BAA0B;EAC1B,kCAAkC;AACpC;;AAEA;EACE;IACE,yBAAyB;EAC3B;AACF;;AAEA;EACE,OAAO;EACP,aAAa;EACb,mCAAmC;EACnC,mBAAmB;EACnB,gBAAgB;EAChB,gBAAgB;EAChB,iBAAiB;EACjB,kBAAkB;EAClB,gDAAgD;EAChD,8CAA8C;EAC9C,+CAA+C;EAC/C,kBAAkB;EAClB,iBAAiB;EACjB,WAAW;EACX,sBAAsB;EACtB,yCAAyC;EACzC,iBAAiB;EACjB,wCAAwC;AAC1C;;AAEA;EACE,yCAAyC;EACzC,eAAe;AACjB;;AAEA;EACE,wCAAwC;EACxC,uCAAuC;AACzC;;AAEA;;EAEE,gBAAgB;EAChB,uBAAuB;EACvB,mBAAmB;AACrB;;AAEA;EACE,gBAAgB;AAClB;;AAEA;EACE,aAAa;EACb,mCAAmC;EACnC,mBAAmB;EACnB,kBAAkB;EAClB,iBAAiB;EACjB,kBAAkB;EAClB,iBAAiB;EACjB,oBAAoB;EACpB,yCAAyC;EACzC,cAAc;EACd,yBAAyB;EACzB,4BAA4B;EAC5B,2BAA2B;EAC3B,gBAAgB;AAClB;;AAEA;EACE,UAAU;EACV,WAAW;AACb;;AAEA;EACE,mBAAmB;EACnB,kBAAkB;AACpB;;AAEA;EACE,0CAA0C;EAC1C,kBAAkB;EAClB,6BAA6B;EAC7B,4BAA4B;AAC9B","sourcesContent":[".mljar-packages-manager-sidebar-container {\n  display: flex;\n  flex-direction: column;\n  height: 100%;\n  overflow-y: auto;\n}\n\n.mljar-packages-manager-search-bar-container {\n  margin: 0px 10px 10px 0px;\n}\n.mljar-packages-manager-install-input,\n.mljar-packages-manager-search-bar-input {\n  width: 100%;\n  padding: 8px;\n  box-sizing: border-box;\n  background-color: var(--jp-layout-color1);\n  color: var(--jp-ui-font-color1);\n  border: 1px solid var(--jp-border-color2);\n  border-radius: 5px;\n}\n\n.mljar-packages-manager-install-input {\n  margin-bottom: 8px;\n}\n\n.mljar-packages-manager-install-input:focus,\n.mljar-packages-manager-search-bar-input:focus {\n  outline: none;\n  border: 2px solid var(--jp-ui-font-color1);\n}\n.mljar-packages-manager-install-input::placeholder,\n.mljar-packages-manager-search-bar-input::placeholder {\n  color: var(--jp-ui-font-color2);\n}\n\n.mljar-packages-manager-container {\n  display: flex;\n  flex-direction: column;\n  height: 100%;\n}\n\n.mljar-packages-manager-header-container {\n  display: flex;\n  justify-content: space-between;\n  align-items: flex-end;\n  margin-bottom: 8px;\n  margin-right: 8px;\n  border-bottom: 2px solid #ddd;\n}\n\n.mljar-packages-manager-header {\n  flex: 4;\n  font-size: 0.85rem;\n  font-weight: 700;\n  color: var(--jp-ui-font-color1);\n  text-align: left;\n  padding-bottom: 8px;\n  margin: 0;\n}\n\n.mljar-packages-manager-list-container {\n  flex: 1;\n  overflow-y: hidden;\n  padding-right: 10px;\n}\n\n.mljar-packages-manager-list {\n  list-style: none;\n  padding: 0;\n  margin: 0;\n}\n\n.mljar-packages-manager-list-container::-webkit-scrollbar {\n  width: 8px;\n}\n\n.mljar-packages-manager-list-container::-webkit-scrollbar-thumb {\n  background-color: rgba(0, 0, 0, 0.2);\n  border-radius: 4px;\n}\n\n.mljar-packages-manager-list-container::-webkit-scrollbar-track {\n  background-color: rgba(0, 0, 0, 0.05);\n}\n\n.mljar-packages-manager-sidebar-widget {\n  background-color: #ffffff;\n  padding: 10px;\n  font-family: 'Courier New', Courier, monospace;\n}\n\n.mljar-packages-manager-back-button,\n.mljar-packages-manager-install-button,\n.mljar-packages-manager-refresh-button {\n  width: 30px;\n  display: flex;\n  margin: 1px 0px 2px 0px;\n  align-items: center;\n  justify-content: center;\n  gap: 8px;\n  color: #0099cc;\n  border: none;\n  border-radius: 4px;\n  padding: 8px 0px;\n  cursor: pointer;\n  font-size: 0.75rem;\n  transition: background-color 0.3s ease;\n}\n\n.mljar-packages-manager-back-button {\n  width: 70px !important;\n  text-align: center;\n  padding-right: 4px;\n}\n\n.mljar-packages-manager-back-button:hover:not(:disabled),\n.mljar-packages-manager-refresh-button:hover:not(:disabled),\n.mljar-packages-manager-install-button:hover:not(:disabled) {\n  background-color: #0099cc;\n  color: #ffffff;\n}\n\n.mljar-packages-manager-delete-button {\n  visibility: hidden;\n  background: none;\n  position: relative;\n  border: none;\n  border-radius: 4px;\n  cursor: pointer;\n  padding: 4px;\n  margin: 5px auto;\n  display: flex;\n  align-items: center;\n  justify-content: center;\n  color: #dc3545;\n  transition: background-color 0.3s ease;\n}\n\n.mljar-packages-manager-refresh-button:disabled,\n.mljar-packages-manager-install-button:disabled,\n.mljar-packages-manager-back-button:disabled {\n  cursor: not-allowed;\n}\n\n.mljar-packages-manager-install-submit-button {\n  display: flex;\n  align-items: center;\n  justify-content: center;\n  background-color: #28a745;\n  color: white;\n  border: none;\n  border-radius: 4px;\n  padding: 8px 12px;\n  cursor: pointer;\n  font-size: 0.75rem;\n  transition: background-color 0.3s ease;\n}\n\n.mljar-packages-manager-install-submit-button:disabled {\n  background-color: #94d3a2;\n  cursor: not-allowed;\n}\n\n.mljar-packages-manager-install-submit-button:hover:not(:disabled) {\n  background-color: #1e7e34;\n}\n\n.mljar-packages-manager-delete-button:hover {\n  color: #fff;\n  background-color: #dc3545;\n  transition: background-color 0.3s ease;\n}\n\n.mljar-packages-manager-list-item:hover .mljar-packages-manager-delete-button {\n  visibility: visible;\n}\n\n.mljar-packages-manager-refresh-icon,\n.mljar-packages-manager-install-icon,\n.mljar-packages-manager-back-icon {\n  display: flex;\n  align-items: center;\n  width: 15px;\n  height: 15px;\n}\n\n.mljar-packages-manager-delete-icon {\n  display: flex;\n  align-items: center;\n  width: 20px;\n  height: 20px;\n}\n\n.mljar-packages-manager-error-icon {\n  color: #dc3545;\n  width: 15px;\n  height: 15px;\n}\n\n.mljar-packages-manager-info-icon-container {\n  position: relative;\n  display: inline-block;\n  cursor: pointer;\n}\n\n.mljar-packages-manager-info-icon-container span:first-child {\n  display: inline-flex;\n  align-items: center;\n  color: #0099cc;\n  margin: 0px;\n  width: 18px;\n  height: 18px;\n}\n\n.mljar-packages-manager-info-icon-container {\n  visibility: hidden;\n  width: 150px;\n  background-color: #28a745;\n  color: white;\n  text-align: center;\n  border-radius: 4px;\n  padding: 5px;\n  position: absolute;\n  left: -160px;\n  top: 100%;\n  z-index: 1;\n  opacity: 0;\n  transition: opacity 0.3s;\n  white-space: pre-line;\n}\n\n.mljar-packages-manager-info-icon-container:hover {\n  visibility: visible;\n  opacity: 1;\n}\n\n.mljar-packages-manager-install-form {\n  display: flex;\n  flex-direction: column;\n  margin-right: 8px;\n}\n\n.mljar-packages-manager-install-form h4 {\n  margin-top: 0px;\n  margin-bottom: 4px;\n  padding: 0;\n}\n\n.mljar-packages-manager-usage-span {\n  margin-bottom: 8px;\n  text-align: left;\n  font-size: 0.8rem;\n  padding: 5px 2px;\n}\n\n.mljar-packages-manager-install-message {\n  color: #28a745;\n  font-weight: bold;\n  margin-top: 10px;\n  text-align: left;\n  padding: 5px 2px;\n}\n\n.mljar-packages-manager-install-message.error {\n  color: #dc3545;\n}\n\n.mljar-packages-manager-error-message {\n  color: #dc3545;\n  font-weight: bold;\n}\n\n.mljar-packages-manager-spinner-container {\n  display: flex;\n  justify-content: center;\n  align-items: center;\n  height: 100%;\n  padding: 20px;\n}\n\n.mljar-packages-manager-spinner {\n  border: 4px solid rgba(0, 0, 0, 0.1);\n  width: 10px;\n  height: 10px;\n  border-radius: 50%;\n  border-left-color: #ffffff;\n  animation: spin 1s linear infinite;\n}\n\n@keyframes spin {\n  to {\n    transform: rotate(360deg);\n  }\n}\n\n.mljar-packages-manager-list-item {\n  flex: 1;\n  display: grid;\n  grid-template-columns: 1fr 1fr 2rem;\n  align-items: center;\n  min-height: 38px;\n  column-gap: 1rem;\n  padding-left: 8px;\n  padding-right: 8px;\n  border-bottom: 1px solid var(--jp-border-color2);\n  border-left: 1px solid var(--jp-border-color2);\n  border-right: 1px solid var(--jp-border-color2);\n  margin-bottom: 0px;\n  margin-right: 0px;\n  width: 100%;\n  box-sizing: border-box;\n  background-color: var(--jp-layout-color0);\n  font-size: 0.7rem;\n  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);\n}\n\n.mljar-packages-manager-list-item:hover {\n  background-color: var(--jp-layout-color2);\n  cursor: pointer;\n}\n\n.mljar-packages-manager-list-item.active {\n  background-color: var(--jp-brand-color1);\n  color: var(--jp-ui-inverse-font-color1);\n}\n\n.mljar-packages-manager-package-name,\n.mljar-packages-manager-package-version {\n  overflow: hidden;\n  text-overflow: ellipsis;\n  white-space: nowrap;\n}\n\n.mljar-packages-manager-package-name {\n  font-weight: 600;\n}\n\n.mljar-packages-manager-list-header {\n  display: grid;\n  grid-template-columns: 1fr 1fr 2rem;\n  align-items: center;\n  font-size: 0.85rem;\n  padding-left: 8px;\n  padding-right: 8px;\n  padding-top: 10px;\n  padding-bottom: 10px;\n  background-color: var(--jp-layout-color0);\n  color: #0099cc;\n  border: 1px solid #0099cc;\n  border-top-right-radius: 5px;\n  border-top-left-radius: 5px;\n  font-weight: 800;\n}\n\n.mljar-packages-manager-sidebar-container::-webkit-scrollbar {\n  width: 8px;\n  height: 8px;\n}\n\n.mljar-packages-manager-sidebar-container::-webkit-scrollbar-track {\n  background: #d3d3d3;\n  border-radius: 8px;\n}\n\n.mljar-packages-manager-sidebar-container::-webkit-scrollbar-thumb {\n  background-color: rgba(255, 255, 255, 0.6);\n  border-radius: 8px;\n  border: 2px solid transparent;\n  background-clip: padding-box;\n}\n"],"sourceRoot":""}]);
// Exports
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (___CSS_LOADER_EXPORT___);


/***/ }),

/***/ "./node_modules/css-loader/dist/runtime/api.js":
/*!*****************************************************!*\
  !*** ./node_modules/css-loader/dist/runtime/api.js ***!
  \*****************************************************/
/***/ ((module) => {



/*
  MIT License http://www.opensource.org/licenses/mit-license.php
  Author Tobias Koppers @sokra
*/
module.exports = function (cssWithMappingToString) {
  var list = [];

  // return the list of modules as css string
  list.toString = function toString() {
    return this.map(function (item) {
      var content = "";
      var needLayer = typeof item[5] !== "undefined";
      if (item[4]) {
        content += "@supports (".concat(item[4], ") {");
      }
      if (item[2]) {
        content += "@media ".concat(item[2], " {");
      }
      if (needLayer) {
        content += "@layer".concat(item[5].length > 0 ? " ".concat(item[5]) : "", " {");
      }
      content += cssWithMappingToString(item);
      if (needLayer) {
        content += "}";
      }
      if (item[2]) {
        content += "}";
      }
      if (item[4]) {
        content += "}";
      }
      return content;
    }).join("");
  };

  // import a list of modules into the list
  list.i = function i(modules, media, dedupe, supports, layer) {
    if (typeof modules === "string") {
      modules = [[null, modules, undefined]];
    }
    var alreadyImportedModules = {};
    if (dedupe) {
      for (var k = 0; k < this.length; k++) {
        var id = this[k][0];
        if (id != null) {
          alreadyImportedModules[id] = true;
        }
      }
    }
    for (var _k = 0; _k < modules.length; _k++) {
      var item = [].concat(modules[_k]);
      if (dedupe && alreadyImportedModules[item[0]]) {
        continue;
      }
      if (typeof layer !== "undefined") {
        if (typeof item[5] === "undefined") {
          item[5] = layer;
        } else {
          item[1] = "@layer".concat(item[5].length > 0 ? " ".concat(item[5]) : "", " {").concat(item[1], "}");
          item[5] = layer;
        }
      }
      if (media) {
        if (!item[2]) {
          item[2] = media;
        } else {
          item[1] = "@media ".concat(item[2], " {").concat(item[1], "}");
          item[2] = media;
        }
      }
      if (supports) {
        if (!item[4]) {
          item[4] = "".concat(supports);
        } else {
          item[1] = "@supports (".concat(item[4], ") {").concat(item[1], "}");
          item[4] = supports;
        }
      }
      list.push(item);
    }
  };
  return list;
};

/***/ }),

/***/ "./node_modules/css-loader/dist/runtime/sourceMaps.js":
/*!************************************************************!*\
  !*** ./node_modules/css-loader/dist/runtime/sourceMaps.js ***!
  \************************************************************/
/***/ ((module) => {



module.exports = function (item) {
  var content = item[1];
  var cssMapping = item[3];
  if (!cssMapping) {
    return content;
  }
  if (typeof btoa === "function") {
    var base64 = btoa(unescape(encodeURIComponent(JSON.stringify(cssMapping))));
    var data = "sourceMappingURL=data:application/json;charset=utf-8;base64,".concat(base64);
    var sourceMapping = "/*# ".concat(data, " */");
    return [content].concat([sourceMapping]).join("\n");
  }
  return [content].join("\n");
};

/***/ }),

/***/ "./node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js":
/*!****************************************************************************!*\
  !*** ./node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js ***!
  \****************************************************************************/
/***/ ((module) => {



var stylesInDOM = [];
function getIndexByIdentifier(identifier) {
  var result = -1;
  for (var i = 0; i < stylesInDOM.length; i++) {
    if (stylesInDOM[i].identifier === identifier) {
      result = i;
      break;
    }
  }
  return result;
}
function modulesToDom(list, options) {
  var idCountMap = {};
  var identifiers = [];
  for (var i = 0; i < list.length; i++) {
    var item = list[i];
    var id = options.base ? item[0] + options.base : item[0];
    var count = idCountMap[id] || 0;
    var identifier = "".concat(id, " ").concat(count);
    idCountMap[id] = count + 1;
    var indexByIdentifier = getIndexByIdentifier(identifier);
    var obj = {
      css: item[1],
      media: item[2],
      sourceMap: item[3],
      supports: item[4],
      layer: item[5]
    };
    if (indexByIdentifier !== -1) {
      stylesInDOM[indexByIdentifier].references++;
      stylesInDOM[indexByIdentifier].updater(obj);
    } else {
      var updater = addElementStyle(obj, options);
      options.byIndex = i;
      stylesInDOM.splice(i, 0, {
        identifier: identifier,
        updater: updater,
        references: 1
      });
    }
    identifiers.push(identifier);
  }
  return identifiers;
}
function addElementStyle(obj, options) {
  var api = options.domAPI(options);
  api.update(obj);
  var updater = function updater(newObj) {
    if (newObj) {
      if (newObj.css === obj.css && newObj.media === obj.media && newObj.sourceMap === obj.sourceMap && newObj.supports === obj.supports && newObj.layer === obj.layer) {
        return;
      }
      api.update(obj = newObj);
    } else {
      api.remove();
    }
  };
  return updater;
}
module.exports = function (list, options) {
  options = options || {};
  list = list || [];
  var lastIdentifiers = modulesToDom(list, options);
  return function update(newList) {
    newList = newList || [];
    for (var i = 0; i < lastIdentifiers.length; i++) {
      var identifier = lastIdentifiers[i];
      var index = getIndexByIdentifier(identifier);
      stylesInDOM[index].references--;
    }
    var newLastIdentifiers = modulesToDom(newList, options);
    for (var _i = 0; _i < lastIdentifiers.length; _i++) {
      var _identifier = lastIdentifiers[_i];
      var _index = getIndexByIdentifier(_identifier);
      if (stylesInDOM[_index].references === 0) {
        stylesInDOM[_index].updater();
        stylesInDOM.splice(_index, 1);
      }
    }
    lastIdentifiers = newLastIdentifiers;
  };
};

/***/ }),

/***/ "./node_modules/style-loader/dist/runtime/insertBySelector.js":
/*!********************************************************************!*\
  !*** ./node_modules/style-loader/dist/runtime/insertBySelector.js ***!
  \********************************************************************/
/***/ ((module) => {



var memo = {};

/* istanbul ignore next  */
function getTarget(target) {
  if (typeof memo[target] === "undefined") {
    var styleTarget = document.querySelector(target);

    // Special case to return head of iframe instead of iframe itself
    if (window.HTMLIFrameElement && styleTarget instanceof window.HTMLIFrameElement) {
      try {
        // This will throw an exception if access to iframe is blocked
        // due to cross-origin restrictions
        styleTarget = styleTarget.contentDocument.head;
      } catch (e) {
        // istanbul ignore next
        styleTarget = null;
      }
    }
    memo[target] = styleTarget;
  }
  return memo[target];
}

/* istanbul ignore next  */
function insertBySelector(insert, style) {
  var target = getTarget(insert);
  if (!target) {
    throw new Error("Couldn't find a style target. This probably means that the value for the 'insert' parameter is invalid.");
  }
  target.appendChild(style);
}
module.exports = insertBySelector;

/***/ }),

/***/ "./node_modules/style-loader/dist/runtime/insertStyleElement.js":
/*!**********************************************************************!*\
  !*** ./node_modules/style-loader/dist/runtime/insertStyleElement.js ***!
  \**********************************************************************/
/***/ ((module) => {



/* istanbul ignore next  */
function insertStyleElement(options) {
  var element = document.createElement("style");
  options.setAttributes(element, options.attributes);
  options.insert(element, options.options);
  return element;
}
module.exports = insertStyleElement;

/***/ }),

/***/ "./node_modules/style-loader/dist/runtime/setAttributesWithoutAttributes.js":
/*!**********************************************************************************!*\
  !*** ./node_modules/style-loader/dist/runtime/setAttributesWithoutAttributes.js ***!
  \**********************************************************************************/
/***/ ((module, __unused_webpack_exports, __webpack_require__) => {



/* istanbul ignore next  */
function setAttributesWithoutAttributes(styleElement) {
  var nonce =  true ? __webpack_require__.nc : 0;
  if (nonce) {
    styleElement.setAttribute("nonce", nonce);
  }
}
module.exports = setAttributesWithoutAttributes;

/***/ }),

/***/ "./node_modules/style-loader/dist/runtime/styleDomAPI.js":
/*!***************************************************************!*\
  !*** ./node_modules/style-loader/dist/runtime/styleDomAPI.js ***!
  \***************************************************************/
/***/ ((module) => {



/* istanbul ignore next  */
function apply(styleElement, options, obj) {
  var css = "";
  if (obj.supports) {
    css += "@supports (".concat(obj.supports, ") {");
  }
  if (obj.media) {
    css += "@media ".concat(obj.media, " {");
  }
  var needLayer = typeof obj.layer !== "undefined";
  if (needLayer) {
    css += "@layer".concat(obj.layer.length > 0 ? " ".concat(obj.layer) : "", " {");
  }
  css += obj.css;
  if (needLayer) {
    css += "}";
  }
  if (obj.media) {
    css += "}";
  }
  if (obj.supports) {
    css += "}";
  }
  var sourceMap = obj.sourceMap;
  if (sourceMap && typeof btoa !== "undefined") {
    css += "\n/*# sourceMappingURL=data:application/json;base64,".concat(btoa(unescape(encodeURIComponent(JSON.stringify(sourceMap)))), " */");
  }

  // For old IE
  /* istanbul ignore if  */
  options.styleTagTransform(css, styleElement, options.options);
}
function removeStyleElement(styleElement) {
  // istanbul ignore if
  if (styleElement.parentNode === null) {
    return false;
  }
  styleElement.parentNode.removeChild(styleElement);
}

/* istanbul ignore next  */
function domAPI(options) {
  if (typeof document === "undefined") {
    return {
      update: function update() {},
      remove: function remove() {}
    };
  }
  var styleElement = options.insertStyleElement(options);
  return {
    update: function update(obj) {
      apply(styleElement, options, obj);
    },
    remove: function remove() {
      removeStyleElement(styleElement);
    }
  };
}
module.exports = domAPI;

/***/ }),

/***/ "./node_modules/style-loader/dist/runtime/styleTagTransform.js":
/*!*********************************************************************!*\
  !*** ./node_modules/style-loader/dist/runtime/styleTagTransform.js ***!
  \*********************************************************************/
/***/ ((module) => {



/* istanbul ignore next  */
function styleTagTransform(css, styleElement) {
  if (styleElement.styleSheet) {
    styleElement.styleSheet.cssText = css;
  } else {
    while (styleElement.firstChild) {
      styleElement.removeChild(styleElement.firstChild);
    }
    styleElement.appendChild(document.createTextNode(css));
  }
}
module.exports = styleTagTransform;

/***/ }),

/***/ "./style/base.css":
/*!************************!*\
  !*** ./style/base.css ***!
  \************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js */ "./node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_styleDomAPI_js__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/styleDomAPI.js */ "./node_modules/style-loader/dist/runtime/styleDomAPI.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_styleDomAPI_js__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_styleDomAPI_js__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_insertBySelector_js__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/insertBySelector.js */ "./node_modules/style-loader/dist/runtime/insertBySelector.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_insertBySelector_js__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_insertBySelector_js__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_setAttributesWithoutAttributes_js__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/setAttributesWithoutAttributes.js */ "./node_modules/style-loader/dist/runtime/setAttributesWithoutAttributes.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_setAttributesWithoutAttributes_js__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_setAttributesWithoutAttributes_js__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_insertStyleElement_js__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/insertStyleElement.js */ "./node_modules/style-loader/dist/runtime/insertStyleElement.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_insertStyleElement_js__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_insertStyleElement_js__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_styleTagTransform_js__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/styleTagTransform.js */ "./node_modules/style-loader/dist/runtime/styleTagTransform.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_styleTagTransform_js__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_styleTagTransform_js__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var _node_modules_css_loader_dist_cjs_js_base_css__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! !!../node_modules/css-loader/dist/cjs.js!./base.css */ "./node_modules/css-loader/dist/cjs.js!./style/base.css");

      
      
      
      
      
      
      
      
      

var options = {};

options.styleTagTransform = (_node_modules_style_loader_dist_runtime_styleTagTransform_js__WEBPACK_IMPORTED_MODULE_5___default());
options.setAttributes = (_node_modules_style_loader_dist_runtime_setAttributesWithoutAttributes_js__WEBPACK_IMPORTED_MODULE_3___default());

      options.insert = _node_modules_style_loader_dist_runtime_insertBySelector_js__WEBPACK_IMPORTED_MODULE_2___default().bind(null, "head");
    
options.domAPI = (_node_modules_style_loader_dist_runtime_styleDomAPI_js__WEBPACK_IMPORTED_MODULE_1___default());
options.insertStyleElement = (_node_modules_style_loader_dist_runtime_insertStyleElement_js__WEBPACK_IMPORTED_MODULE_4___default());

var update = _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0___default()(_node_modules_css_loader_dist_cjs_js_base_css__WEBPACK_IMPORTED_MODULE_6__["default"], options);




       /* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (_node_modules_css_loader_dist_cjs_js_base_css__WEBPACK_IMPORTED_MODULE_6__["default"] && _node_modules_css_loader_dist_cjs_js_base_css__WEBPACK_IMPORTED_MODULE_6__["default"].locals ? _node_modules_css_loader_dist_cjs_js_base_css__WEBPACK_IMPORTED_MODULE_6__["default"].locals : undefined);


/***/ }),

/***/ "./style/index.js":
/*!************************!*\
  !*** ./style/index.js ***!
  \************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony import */ var _base_css__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./base.css */ "./style/base.css");



/***/ })

}]);
//# sourceMappingURL=style_index_js.489cc3c6be8c31f8bd37.js.map