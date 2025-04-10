"use strict";
(self["webpackChunkdotscripts"] = self["webpackChunkdotscripts"] || []).push([["lib_index_js"],{

/***/ "./lib/index.js":
/*!**********************!*\
  !*** ./lib/index.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/notebook */ "webpack/sharing/consume/default/@jupyterlab/notebook");
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__);

const extension = {
    id: 'dotscripts',
    autoStart: true,
    requires: [_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__.INotebookTracker],
    activate: (app, notebooks) => {
        console.log('✅ JupyterLab extension dotscripts is activated.');
        const command = 'dotscripts:run-tagged-and-below';
        app.commands.addCommand(command, {
            label: 'Run Tagged Cell and All Below (No Scrolling)',
            execute: async (args) => {
                const tagName = args.tag || 'my-tag';
                // ✅ Create and show loading overlay with a spinner
                const overlay = document.createElement('div');
                overlay.style.position = 'fixed';
                overlay.style.top = '0';
                overlay.style.left = '0';
                overlay.style.width = '100%';
                overlay.style.height = '100%';
                overlay.style.backgroundColor = 'rgba(0, 0, 0, 0.3)';
                overlay.style.display = 'flex';
                overlay.style.alignItems = 'center';
                overlay.style.justifyContent = 'center';
                overlay.style.zIndex = '10000';
                overlay.innerHTML = `
          <div style="background: white; padding: 20px; border-radius: 10px; text-align: center; display: flex; flex-direction: column; align-items: center;">
            <p>Calculation running...</p>
            <div class="spinner" style="border: 4px solid rgba(0,0,0,0.1); border-left-color: black; width: 40px; height: 40px; border-radius: 50%; animation: spin 1s linear infinite;"></div>
            <style>
              @keyframes spin {
                from { transform: rotate(0deg); }
                to { transform: rotate(360deg); }
              }
            </style>
          </div>
        `;
                document.body.appendChild(overlay);
                // ✅ 1. Find all scrollable containers
                const scrollContainers = document.querySelectorAll('.jp-WindowedPanel-outer');
                const activeCells = document.querySelectorAll('.jp-Cell.jp-CodeCell');
                const previousScrollPositions = new Map();
                // ✅ 2. Disable scrolling (lock scrollTop)
                const disableScrolling = () => {
                    scrollContainers.forEach(el => {
                        previousScrollPositions.set(el, el.scrollTop);
                        el.style.overflow = 'hidden';
                        el.dataset.lockScroll = 'true';
                    });
                    activeCells.forEach(cell => {
                        cell.setAttribute('tabindex', '-1');
                    });
                    document.addEventListener('scroll', preventForcedScroll, true);
                };
                const enableScrolling = () => {
                    scrollContainers.forEach(el => {
                        el.style.overflow = '';
                        el.scrollTop = previousScrollPositions.get(el) || 0;
                        el.dataset.lockScroll = 'false';
                    });
                    activeCells.forEach(cell => {
                        cell.setAttribute('tabindex', '0');
                    });
                    document.removeEventListener('scroll', preventForcedScroll, true);
                };
                const preventForcedScroll = (event) => {
                    const target = event.target;
                    if (target.dataset.lockScroll === 'true') {
                        target.scrollTop = previousScrollPositions.get(target) || 0;
                        event.preventDefault();
                    }
                };
                disableScrolling();
                await new Promise(resolve => setTimeout(resolve, 0));
                try {
                    const current = notebooks.currentWidget;
                    if (!current) {
                        document.body.removeChild(overlay);
                        return;
                    }
                    const notebook = current.content;
                    for (let index = 0; index < notebook.widgets.length; index++) {
                        const cell = notebook.widgets[index];
                        const tags = cell.model.metadata?.tags;
                        if (Array.isArray(tags) && tags.includes(tagName)) {
                            notebook.activeCellIndex = index;
                            await app.commands.execute('notebook:run-all-below');
                            document.body.removeChild(overlay);
                            return;
                        }
                    }
                }
                catch (error) {
                    document.body.removeChild(overlay);
                }
                finally {
                    enableScrolling();
                }
            }
        });
    }
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (extension);


/***/ })

}]);
//# sourceMappingURL=lib_index_js.6e8f095b827fdc447c56.js.map