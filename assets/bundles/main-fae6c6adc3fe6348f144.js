/******/ (function(modules) { // webpackBootstrap
/******/ 	// The module cache
/******/ 	var installedModules = {};
/******/
/******/ 	// The require function
/******/ 	function __webpack_require__(moduleId) {
/******/
/******/ 		// Check if module is in cache
/******/ 		if(installedModules[moduleId]) {
/******/ 			return installedModules[moduleId].exports;
/******/ 		}
/******/ 		// Create a new module (and put it into the cache)
/******/ 		var module = installedModules[moduleId] = {
/******/ 			i: moduleId,
/******/ 			l: false,
/******/ 			exports: {}
/******/ 		};
/******/
/******/ 		// Execute the module function
/******/ 		modules[moduleId].call(module.exports, module, module.exports, __webpack_require__);
/******/
/******/ 		// Flag the module as loaded
/******/ 		module.l = true;
/******/
/******/ 		// Return the exports of the module
/******/ 		return module.exports;
/******/ 	}
/******/
/******/
/******/ 	// expose the modules object (__webpack_modules__)
/******/ 	__webpack_require__.m = modules;
/******/
/******/ 	// expose the module cache
/******/ 	__webpack_require__.c = installedModules;
/******/
/******/ 	// define getter function for harmony exports
/******/ 	__webpack_require__.d = function(exports, name, getter) {
/******/ 		if(!__webpack_require__.o(exports, name)) {
/******/ 			Object.defineProperty(exports, name, {
/******/ 				configurable: false,
/******/ 				enumerable: true,
/******/ 				get: getter
/******/ 			});
/******/ 		}
/******/ 	};
/******/
/******/ 	// getDefaultExport function for compatibility with non-harmony modules
/******/ 	__webpack_require__.n = function(module) {
/******/ 		var getter = module && module.__esModule ?
/******/ 			function getDefault() { return module['default']; } :
/******/ 			function getModuleExports() { return module; };
/******/ 		__webpack_require__.d(getter, 'a', getter);
/******/ 		return getter;
/******/ 	};
/******/
/******/ 	// Object.prototype.hasOwnProperty.call
/******/ 	__webpack_require__.o = function(object, property) { return Object.prototype.hasOwnProperty.call(object, property); };
/******/
/******/ 	// __webpack_public_path__
/******/ 	__webpack_require__.p = "";
/******/
/******/ 	// Load entry module and return exports
/******/ 	return __webpack_require__(__webpack_require__.s = 0);
/******/ })
/************************************************************************/
/******/ ([
/* 0 */
/***/ (function(module, exports) {

throw new Error("Module build failed: SyntaxError: /home/sidney/Dropbox/CML/1software_dev/Django/CMLMasterProject/.babelrc: Error while parsing JSON - Unexpected EOF at line 1 column 2 of the JSON5 data. Still to read: \"\"\n    at error (/home/sidney/Dropbox/CML/1software_dev/Django/CMLMasterProject/node_modules/json5/lib/json5.js:56:25)\n    at word (/home/sidney/Dropbox/CML/1software_dev/Django/CMLMasterProject/node_modules/json5/lib/json5.js:393:13)\n    at value (/home/sidney/Dropbox/CML/1software_dev/Django/CMLMasterProject/node_modules/json5/lib/json5.js:493:56)\n    at Object.parse (/home/sidney/Dropbox/CML/1software_dev/Django/CMLMasterProject/node_modules/json5/lib/json5.js:508:18)\n    at ConfigChainBuilder.addConfig (/home/sidney/Dropbox/CML/1software_dev/Django/CMLMasterProject/node_modules/babel-core/lib/transformation/file/options/build-config-chain.js:150:65)\n    at ConfigChainBuilder.findConfigs (/home/sidney/Dropbox/CML/1software_dev/Django/CMLMasterProject/node_modules/babel-core/lib/transformation/file/options/build-config-chain.js:96:16)\n    at buildConfigChain (/home/sidney/Dropbox/CML/1software_dev/Django/CMLMasterProject/node_modules/babel-core/lib/transformation/file/options/build-config-chain.js:61:13)\n    at OptionManager.init (/home/sidney/Dropbox/CML/1software_dev/Django/CMLMasterProject/node_modules/babel-core/lib/transformation/file/options/option-manager.js:354:58)\n    at File.initOptions (/home/sidney/Dropbox/CML/1software_dev/Django/CMLMasterProject/node_modules/babel-core/lib/transformation/file/index.js:212:65)\n    at new File (/home/sidney/Dropbox/CML/1software_dev/Django/CMLMasterProject/node_modules/babel-core/lib/transformation/file/index.js:135:24)\n    at Pipeline.transform (/home/sidney/Dropbox/CML/1software_dev/Django/CMLMasterProject/node_modules/babel-core/lib/transformation/pipeline.js:46:16)\n    at transpile (/home/sidney/Dropbox/CML/1software_dev/Django/CMLMasterProject/node_modules/babel-loader/lib/index.js:50:20)\n    at Object.module.exports (/home/sidney/Dropbox/CML/1software_dev/Django/CMLMasterProject/node_modules/babel-loader/lib/index.js:175:20)");

/***/ })
/******/ ]);