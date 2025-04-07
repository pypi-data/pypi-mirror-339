var __defProp = Object.defineProperty;
var __name = (target, value) => __defProp(target, "name", { value, configurable: true });
import { cz as BaseStyle, cZ as script$6, f as createElementBlock, o as openBlock, aL as mergeProps, m as createBaseVNode, d0 as script$7, cM as Ripple, dD as script$8, dE as script$9, dh as script$a, cA as script$b, cB as cn, r as resolveDirective, y as createBlock, C as resolveDynamicComponent, A as createCommentVNode, F as Fragment, I as toDisplayString, dv as normalizeProps, i as withDirectives, d1 as setAttribute, dj as isEmpty, db as ZIndex, dZ as ToastEventBus, cL as resolveComponent, z as withCtx, k as createVNode, d_ as TransitionGroup, G as renderList, s as script$c, dw as FocusTrap, dx as unblockBodyScroll, dz as blockBodyScroll, cP as focus, cV as addClass, cr as Transition, B as renderSlot, a5 as normalizeClass } from "./index-C3Y6Vd_l.js";
var style$1 = /* @__PURE__ */ __name(({ dt: o }) => `
.p-toast {
    width: ${o("toast.width")};
    white-space: pre-line;
    word-break: break-word;
}

.p-toast-message {
    margin: 0 0 1rem 0;
}

.p-toast-message-icon {
    flex-shrink: 0;
    font-size: ${o("toast.icon.size")};
    width: ${o("toast.icon.size")};
    height: ${o("toast.icon.size")};
}

.p-toast-message-content {
    display: flex;
    align-items: flex-start;
    padding: ${o("toast.content.padding")};
    gap: ${o("toast.content.gap")};
}

.p-toast-message-text {
    flex: 1 1 auto;
    display: flex;
    flex-direction: column;
    gap: ${o("toast.text.gap")};
}

.p-toast-summary {
    font-weight: ${o("toast.summary.font.weight")};
    font-size: ${o("toast.summary.font.size")};
}

.p-toast-detail {
    font-weight: ${o("toast.detail.font.weight")};
    font-size: ${o("toast.detail.font.size")};
}

.p-toast-close-button {
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
    position: relative;
    cursor: pointer;
    background: transparent;
    transition: background ${o("toast.transition.duration")}, color ${o("toast.transition.duration")}, outline-color ${o("toast.transition.duration")}, box-shadow ${o("toast.transition.duration")};
    outline-color: transparent;
    color: inherit;
    width: ${o("toast.close.button.width")};
    height: ${o("toast.close.button.height")};
    border-radius: ${o("toast.close.button.border.radius")};
    margin: -25% 0 0 0;
    right: -25%;
    padding: 0;
    border: none;
    user-select: none;
}

.p-toast-close-button:dir(rtl) {
    margin: -25% 0 0 auto;
    left: -25%;
    right: auto;
}

.p-toast-message-info,
.p-toast-message-success,
.p-toast-message-warn,
.p-toast-message-error,
.p-toast-message-secondary,
.p-toast-message-contrast {
    border-width: ${o("toast.border.width")};
    border-style: solid;
    backdrop-filter: blur(${o("toast.blur")});
    border-radius: ${o("toast.border.radius")};
}

.p-toast-close-icon {
    font-size: ${o("toast.close.icon.size")};
    width: ${o("toast.close.icon.size")};
    height: ${o("toast.close.icon.size")};
}

.p-toast-close-button:focus-visible {
    outline-width: ${o("focus.ring.width")};
    outline-style: ${o("focus.ring.style")};
    outline-offset: ${o("focus.ring.offset")};
}

.p-toast-message-info {
    background: ${o("toast.info.background")};
    border-color: ${o("toast.info.border.color")};
    color: ${o("toast.info.color")};
    box-shadow: ${o("toast.info.shadow")};
}

.p-toast-message-info .p-toast-detail {
    color: ${o("toast.info.detail.color")};
}

.p-toast-message-info .p-toast-close-button:focus-visible {
    outline-color: ${o("toast.info.close.button.focus.ring.color")};
    box-shadow: ${o("toast.info.close.button.focus.ring.shadow")};
}

.p-toast-message-info .p-toast-close-button:hover {
    background: ${o("toast.info.close.button.hover.background")};
}

.p-toast-message-success {
    background: ${o("toast.success.background")};
    border-color: ${o("toast.success.border.color")};
    color: ${o("toast.success.color")};
    box-shadow: ${o("toast.success.shadow")};
}

.p-toast-message-success .p-toast-detail {
    color: ${o("toast.success.detail.color")};
}

.p-toast-message-success .p-toast-close-button:focus-visible {
    outline-color: ${o("toast.success.close.button.focus.ring.color")};
    box-shadow: ${o("toast.success.close.button.focus.ring.shadow")};
}

.p-toast-message-success .p-toast-close-button:hover {
    background: ${o("toast.success.close.button.hover.background")};
}

.p-toast-message-warn {
    background: ${o("toast.warn.background")};
    border-color: ${o("toast.warn.border.color")};
    color: ${o("toast.warn.color")};
    box-shadow: ${o("toast.warn.shadow")};
}

.p-toast-message-warn .p-toast-detail {
    color: ${o("toast.warn.detail.color")};
}

.p-toast-message-warn .p-toast-close-button:focus-visible {
    outline-color: ${o("toast.warn.close.button.focus.ring.color")};
    box-shadow: ${o("toast.warn.close.button.focus.ring.shadow")};
}

.p-toast-message-warn .p-toast-close-button:hover {
    background: ${o("toast.warn.close.button.hover.background")};
}

.p-toast-message-error {
    background: ${o("toast.error.background")};
    border-color: ${o("toast.error.border.color")};
    color: ${o("toast.error.color")};
    box-shadow: ${o("toast.error.shadow")};
}

.p-toast-message-error .p-toast-detail {
    color: ${o("toast.error.detail.color")};
}

.p-toast-message-error .p-toast-close-button:focus-visible {
    outline-color: ${o("toast.error.close.button.focus.ring.color")};
    box-shadow: ${o("toast.error.close.button.focus.ring.shadow")};
}

.p-toast-message-error .p-toast-close-button:hover {
    background: ${o("toast.error.close.button.hover.background")};
}

.p-toast-message-secondary {
    background: ${o("toast.secondary.background")};
    border-color: ${o("toast.secondary.border.color")};
    color: ${o("toast.secondary.color")};
    box-shadow: ${o("toast.secondary.shadow")};
}

.p-toast-message-secondary .p-toast-detail {
    color: ${o("toast.secondary.detail.color")};
}

.p-toast-message-secondary .p-toast-close-button:focus-visible {
    outline-color: ${o("toast.secondary.close.button.focus.ring.color")};
    box-shadow: ${o("toast.secondary.close.button.focus.ring.shadow")};
}

.p-toast-message-secondary .p-toast-close-button:hover {
    background: ${o("toast.secondary.close.button.hover.background")};
}

.p-toast-message-contrast {
    background: ${o("toast.contrast.background")};
    border-color: ${o("toast.contrast.border.color")};
    color: ${o("toast.contrast.color")};
    box-shadow: ${o("toast.contrast.shadow")};
}

.p-toast-message-contrast .p-toast-detail {
    color: ${o("toast.contrast.detail.color")};
}

.p-toast-message-contrast .p-toast-close-button:focus-visible {
    outline-color: ${o("toast.contrast.close.button.focus.ring.color")};
    box-shadow: ${o("toast.contrast.close.button.focus.ring.shadow")};
}

.p-toast-message-contrast .p-toast-close-button:hover {
    background: ${o("toast.contrast.close.button.hover.background")};
}

.p-toast-top-center {
    transform: translateX(-50%);
}

.p-toast-bottom-center {
    transform: translateX(-50%);
}

.p-toast-center {
    min-width: 20vw;
    transform: translate(-50%, -50%);
}

.p-toast-message-enter-from {
    opacity: 0;
    transform: translateY(50%);
}

.p-toast-message-leave-from {
    max-height: 1000px;
}

.p-toast .p-toast-message.p-toast-message-leave-to {
    max-height: 0;
    opacity: 0;
    margin-bottom: 0;
    overflow: hidden;
}

.p-toast-message-enter-active {
    transition: transform 0.3s, opacity 0.3s;
}

.p-toast-message-leave-active {
    transition: max-height 0.45s cubic-bezier(0, 1, 0, 1), opacity 0.3s, margin-bottom 0.3s;
}
`, "style$1");
function _typeof$5(o) {
  "@babel/helpers - typeof";
  return _typeof$5 = "function" == typeof Symbol && "symbol" == typeof Symbol.iterator ? function(o2) {
    return typeof o2;
  } : function(o2) {
    return o2 && "function" == typeof Symbol && o2.constructor === Symbol && o2 !== Symbol.prototype ? "symbol" : typeof o2;
  }, _typeof$5(o);
}
__name(_typeof$5, "_typeof$5");
function _defineProperty$5(e, r, t) {
  return (r = _toPropertyKey$5(r)) in e ? Object.defineProperty(e, r, { value: t, enumerable: true, configurable: true, writable: true }) : e[r] = t, e;
}
__name(_defineProperty$5, "_defineProperty$5");
function _toPropertyKey$5(t) {
  var i = _toPrimitive$5(t, "string");
  return "symbol" == _typeof$5(i) ? i : i + "";
}
__name(_toPropertyKey$5, "_toPropertyKey$5");
function _toPrimitive$5(t, r) {
  if ("object" != _typeof$5(t) || !t) return t;
  var e = t[Symbol.toPrimitive];
  if (void 0 !== e) {
    var i = e.call(t, r);
    if ("object" != _typeof$5(i)) return i;
    throw new TypeError("@@toPrimitive must return a primitive value.");
  }
  return ("string" === r ? String : Number)(t);
}
__name(_toPrimitive$5, "_toPrimitive$5");
var inlineStyles$1 = {
  root: /* @__PURE__ */ __name(function root(_ref) {
    var position = _ref.position;
    return {
      position: "fixed",
      top: position === "top-right" || position === "top-left" || position === "top-center" ? "20px" : position === "center" ? "50%" : null,
      right: (position === "top-right" || position === "bottom-right") && "20px",
      bottom: (position === "bottom-left" || position === "bottom-right" || position === "bottom-center") && "20px",
      left: position === "top-left" || position === "bottom-left" ? "20px" : position === "center" || position === "top-center" || position === "bottom-center" ? "50%" : null
    };
  }, "root")
};
var classes$1 = {
  root: /* @__PURE__ */ __name(function root2(_ref2) {
    var props = _ref2.props;
    return ["p-toast p-component p-toast-" + props.position];
  }, "root"),
  message: /* @__PURE__ */ __name(function message(_ref3) {
    var props = _ref3.props;
    return ["p-toast-message", {
      "p-toast-message-info": props.message.severity === "info" || props.message.severity === void 0,
      "p-toast-message-warn": props.message.severity === "warn",
      "p-toast-message-error": props.message.severity === "error",
      "p-toast-message-success": props.message.severity === "success",
      "p-toast-message-secondary": props.message.severity === "secondary",
      "p-toast-message-contrast": props.message.severity === "contrast"
    }];
  }, "message"),
  messageContent: "p-toast-message-content",
  messageIcon: /* @__PURE__ */ __name(function messageIcon(_ref4) {
    var props = _ref4.props;
    return ["p-toast-message-icon", _defineProperty$5(_defineProperty$5(_defineProperty$5(_defineProperty$5({}, props.infoIcon, props.message.severity === "info"), props.warnIcon, props.message.severity === "warn"), props.errorIcon, props.message.severity === "error"), props.successIcon, props.message.severity === "success")];
  }, "messageIcon"),
  messageText: "p-toast-message-text",
  summary: "p-toast-summary",
  detail: "p-toast-detail",
  closeButton: "p-toast-close-button",
  closeIcon: "p-toast-close-icon"
};
var ToastStyle = BaseStyle.extend({
  name: "toast",
  style: style$1,
  classes: classes$1,
  inlineStyles: inlineStyles$1
});
var script$5 = {
  name: "ExclamationTriangleIcon",
  "extends": script$6
};
function render$4(_ctx, _cache, $props, $setup, $data, $options) {
  return openBlock(), createElementBlock("svg", mergeProps({
    width: "14",
    height: "14",
    viewBox: "0 0 14 14",
    fill: "none",
    xmlns: "http://www.w3.org/2000/svg"
  }, _ctx.pti()), _cache[0] || (_cache[0] = [createBaseVNode("path", {
    d: "M13.4018 13.1893H0.598161C0.49329 13.189 0.390283 13.1615 0.299143 13.1097C0.208003 13.0578 0.131826 12.9832 0.0780112 12.8932C0.0268539 12.8015 0 12.6982 0 12.5931C0 12.4881 0.0268539 12.3848 0.0780112 12.293L6.47985 1.08982C6.53679 1.00399 6.61408 0.933574 6.70484 0.884867C6.7956 0.836159 6.897 0.810669 7 0.810669C7.103 0.810669 7.2044 0.836159 7.29516 0.884867C7.38592 0.933574 7.46321 1.00399 7.52015 1.08982L13.922 12.293C13.9731 12.3848 14 12.4881 14 12.5931C14 12.6982 13.9731 12.8015 13.922 12.8932C13.8682 12.9832 13.792 13.0578 13.7009 13.1097C13.6097 13.1615 13.5067 13.189 13.4018 13.1893ZM1.63046 11.989H12.3695L7 2.59425L1.63046 11.989Z",
    fill: "currentColor"
  }, null, -1), createBaseVNode("path", {
    d: "M6.99996 8.78801C6.84143 8.78594 6.68997 8.72204 6.57787 8.60993C6.46576 8.49782 6.40186 8.34637 6.39979 8.18784V5.38703C6.39979 5.22786 6.46302 5.0752 6.57557 4.96265C6.68813 4.85009 6.84078 4.78686 6.99996 4.78686C7.15914 4.78686 7.31179 4.85009 7.42435 4.96265C7.5369 5.0752 7.60013 5.22786 7.60013 5.38703V8.18784C7.59806 8.34637 7.53416 8.49782 7.42205 8.60993C7.30995 8.72204 7.15849 8.78594 6.99996 8.78801Z",
    fill: "currentColor"
  }, null, -1), createBaseVNode("path", {
    d: "M6.99996 11.1887C6.84143 11.1866 6.68997 11.1227 6.57787 11.0106C6.46576 10.8985 6.40186 10.7471 6.39979 10.5885V10.1884C6.39979 10.0292 6.46302 9.87658 6.57557 9.76403C6.68813 9.65147 6.84078 9.58824 6.99996 9.58824C7.15914 9.58824 7.31179 9.65147 7.42435 9.76403C7.5369 9.87658 7.60013 10.0292 7.60013 10.1884V10.5885C7.59806 10.7471 7.53416 10.8985 7.42205 11.0106C7.30995 11.1227 7.15849 11.1866 6.99996 11.1887Z",
    fill: "currentColor"
  }, null, -1)]), 16);
}
__name(render$4, "render$4");
script$5.render = render$4;
var script$4 = {
  name: "InfoCircleIcon",
  "extends": script$6
};
function render$3(_ctx, _cache, $props, $setup, $data, $options) {
  return openBlock(), createElementBlock("svg", mergeProps({
    width: "14",
    height: "14",
    viewBox: "0 0 14 14",
    fill: "none",
    xmlns: "http://www.w3.org/2000/svg"
  }, _ctx.pti()), _cache[0] || (_cache[0] = [createBaseVNode("path", {
    "fill-rule": "evenodd",
    "clip-rule": "evenodd",
    d: "M3.11101 12.8203C4.26215 13.5895 5.61553 14 7 14C8.85652 14 10.637 13.2625 11.9497 11.9497C13.2625 10.637 14 8.85652 14 7C14 5.61553 13.5895 4.26215 12.8203 3.11101C12.0511 1.95987 10.9579 1.06266 9.67879 0.532846C8.3997 0.00303296 6.99224 -0.13559 5.63437 0.134506C4.2765 0.404603 3.02922 1.07129 2.05026 2.05026C1.07129 3.02922 0.404603 4.2765 0.134506 5.63437C-0.13559 6.99224 0.00303296 8.3997 0.532846 9.67879C1.06266 10.9579 1.95987 12.0511 3.11101 12.8203ZM3.75918 2.14976C4.71846 1.50879 5.84628 1.16667 7 1.16667C8.5471 1.16667 10.0308 1.78125 11.1248 2.87521C12.2188 3.96918 12.8333 5.45291 12.8333 7C12.8333 8.15373 12.4912 9.28154 11.8502 10.2408C11.2093 11.2001 10.2982 11.9478 9.23232 12.3893C8.16642 12.8308 6.99353 12.9463 5.86198 12.7212C4.73042 12.4962 3.69102 11.9406 2.87521 11.1248C2.05941 10.309 1.50384 9.26958 1.27876 8.13803C1.05367 7.00647 1.16919 5.83358 1.61071 4.76768C2.05222 3.70178 2.79989 2.79074 3.75918 2.14976ZM7.00002 4.8611C6.84594 4.85908 6.69873 4.79698 6.58977 4.68801C6.48081 4.57905 6.4187 4.43185 6.41669 4.27776V3.88888C6.41669 3.73417 6.47815 3.58579 6.58754 3.4764C6.69694 3.367 6.84531 3.30554 7.00002 3.30554C7.15473 3.30554 7.3031 3.367 7.4125 3.4764C7.52189 3.58579 7.58335 3.73417 7.58335 3.88888V4.27776C7.58134 4.43185 7.51923 4.57905 7.41027 4.68801C7.30131 4.79698 7.1541 4.85908 7.00002 4.8611ZM7.00002 10.6945C6.84594 10.6925 6.69873 10.6304 6.58977 10.5214C6.48081 10.4124 6.4187 10.2652 6.41669 10.1111V6.22225C6.41669 6.06754 6.47815 5.91917 6.58754 5.80977C6.69694 5.70037 6.84531 5.63892 7.00002 5.63892C7.15473 5.63892 7.3031 5.70037 7.4125 5.80977C7.52189 5.91917 7.58335 6.06754 7.58335 6.22225V10.1111C7.58134 10.2652 7.51923 10.4124 7.41027 10.5214C7.30131 10.6304 7.1541 10.6925 7.00002 10.6945Z",
    fill: "currentColor"
  }, null, -1)]), 16);
}
__name(render$3, "render$3");
script$4.render = render$3;
var script$2 = {
  name: "BaseToast",
  "extends": script$b,
  props: {
    group: {
      type: String,
      "default": null
    },
    position: {
      type: String,
      "default": "top-right"
    },
    autoZIndex: {
      type: Boolean,
      "default": true
    },
    baseZIndex: {
      type: Number,
      "default": 0
    },
    breakpoints: {
      type: Object,
      "default": null
    },
    closeIcon: {
      type: String,
      "default": void 0
    },
    infoIcon: {
      type: String,
      "default": void 0
    },
    warnIcon: {
      type: String,
      "default": void 0
    },
    errorIcon: {
      type: String,
      "default": void 0
    },
    successIcon: {
      type: String,
      "default": void 0
    },
    closeButtonProps: {
      type: null,
      "default": null
    },
    onMouseEnter: {
      type: Function,
      "default": void 0
    },
    onMouseLeave: {
      type: Function,
      "default": void 0
    },
    onClick: {
      type: Function,
      "default": void 0
    }
  },
  style: ToastStyle,
  provide: /* @__PURE__ */ __name(function provide() {
    return {
      $pcToast: this,
      $parentInstance: this
    };
  }, "provide")
};
function _typeof$3(o) {
  "@babel/helpers - typeof";
  return _typeof$3 = "function" == typeof Symbol && "symbol" == typeof Symbol.iterator ? function(o2) {
    return typeof o2;
  } : function(o2) {
    return o2 && "function" == typeof Symbol && o2.constructor === Symbol && o2 !== Symbol.prototype ? "symbol" : typeof o2;
  }, _typeof$3(o);
}
__name(_typeof$3, "_typeof$3");
function _defineProperty$3(e, r, t) {
  return (r = _toPropertyKey$3(r)) in e ? Object.defineProperty(e, r, { value: t, enumerable: true, configurable: true, writable: true }) : e[r] = t, e;
}
__name(_defineProperty$3, "_defineProperty$3");
function _toPropertyKey$3(t) {
  var i = _toPrimitive$3(t, "string");
  return "symbol" == _typeof$3(i) ? i : i + "";
}
__name(_toPropertyKey$3, "_toPropertyKey$3");
function _toPrimitive$3(t, r) {
  if ("object" != _typeof$3(t) || !t) return t;
  var e = t[Symbol.toPrimitive];
  if (void 0 !== e) {
    var i = e.call(t, r);
    if ("object" != _typeof$3(i)) return i;
    throw new TypeError("@@toPrimitive must return a primitive value.");
  }
  return ("string" === r ? String : Number)(t);
}
__name(_toPrimitive$3, "_toPrimitive$3");
var script$1$1 = {
  name: "ToastMessage",
  hostName: "Toast",
  "extends": script$b,
  emits: ["close"],
  closeTimeout: null,
  createdAt: null,
  lifeRemaining: null,
  props: {
    message: {
      type: null,
      "default": null
    },
    templates: {
      type: Object,
      "default": null
    },
    closeIcon: {
      type: String,
      "default": null
    },
    infoIcon: {
      type: String,
      "default": null
    },
    warnIcon: {
      type: String,
      "default": null
    },
    errorIcon: {
      type: String,
      "default": null
    },
    successIcon: {
      type: String,
      "default": null
    },
    closeButtonProps: {
      type: null,
      "default": null
    }
  },
  mounted: /* @__PURE__ */ __name(function mounted() {
    if (this.message.life) {
      this.lifeRemaining = this.message.life;
      this.startTimeout();
    }
  }, "mounted"),
  beforeUnmount: /* @__PURE__ */ __name(function beforeUnmount() {
    this.clearCloseTimeout();
  }, "beforeUnmount"),
  methods: {
    startTimeout: /* @__PURE__ */ __name(function startTimeout() {
      var _this = this;
      this.createdAt = (/* @__PURE__ */ new Date()).valueOf();
      this.closeTimeout = setTimeout(function() {
        _this.close({
          message: _this.message,
          type: "life-end"
        });
      }, this.lifeRemaining);
    }, "startTimeout"),
    close: /* @__PURE__ */ __name(function close(params) {
      this.$emit("close", params);
    }, "close"),
    onCloseClick: /* @__PURE__ */ __name(function onCloseClick() {
      this.clearCloseTimeout();
      this.close({
        message: this.message,
        type: "close"
      });
    }, "onCloseClick"),
    clearCloseTimeout: /* @__PURE__ */ __name(function clearCloseTimeout() {
      if (this.closeTimeout) {
        clearTimeout(this.closeTimeout);
        this.closeTimeout = null;
      }
    }, "clearCloseTimeout"),
    onMessageClick: /* @__PURE__ */ __name(function onMessageClick(event) {
      var _this$props;
      ((_this$props = this.props) === null || _this$props === void 0 ? void 0 : _this$props.onClick) && this.props.onClick({
        originalEvent: event,
        message: this.message
      });
    }, "onMessageClick"),
    onMouseEnter: /* @__PURE__ */ __name(function onMouseEnter(event) {
      var _this$props2;
      if ((_this$props2 = this.props) !== null && _this$props2 !== void 0 && _this$props2.onMouseEnter) {
        this.props.onMouseEnter({
          originalEvent: event,
          message: this.message
        });
        if (event.defaultPrevented) {
          return;
        }
        if (this.message.life) {
          this.lifeRemaining = this.createdAt + this.lifeRemaining - Date().valueOf();
          this.createdAt = null;
          this.clearCloseTimeout();
        }
      }
    }, "onMouseEnter"),
    onMouseLeave: /* @__PURE__ */ __name(function onMouseLeave(event) {
      var _this$props3;
      if ((_this$props3 = this.props) !== null && _this$props3 !== void 0 && _this$props3.onMouseLeave) {
        this.props.onMouseLeave({
          originalEvent: event,
          message: this.message
        });
        if (event.defaultPrevented) {
          return;
        }
        if (this.message.life) {
          this.startTimeout();
        }
      }
    }, "onMouseLeave")
  },
  computed: {
    iconComponent: /* @__PURE__ */ __name(function iconComponent() {
      return {
        info: !this.infoIcon && script$4,
        success: !this.successIcon && script$9,
        warn: !this.warnIcon && script$5,
        error: !this.errorIcon && script$8
      }[this.message.severity];
    }, "iconComponent"),
    closeAriaLabel: /* @__PURE__ */ __name(function closeAriaLabel() {
      return this.$primevue.config.locale.aria ? this.$primevue.config.locale.aria.close : void 0;
    }, "closeAriaLabel"),
    dataP: /* @__PURE__ */ __name(function dataP() {
      return cn(_defineProperty$3({}, this.message.severity, this.message.severity));
    }, "dataP")
  },
  components: {
    TimesIcon: script$a,
    InfoCircleIcon: script$4,
    CheckIcon: script$9,
    ExclamationTriangleIcon: script$5,
    TimesCircleIcon: script$8
  },
  directives: {
    ripple: Ripple
  }
};
function _typeof$2(o) {
  "@babel/helpers - typeof";
  return _typeof$2 = "function" == typeof Symbol && "symbol" == typeof Symbol.iterator ? function(o2) {
    return typeof o2;
  } : function(o2) {
    return o2 && "function" == typeof Symbol && o2.constructor === Symbol && o2 !== Symbol.prototype ? "symbol" : typeof o2;
  }, _typeof$2(o);
}
__name(_typeof$2, "_typeof$2");
function ownKeys$1(e, r) {
  var t = Object.keys(e);
  if (Object.getOwnPropertySymbols) {
    var o = Object.getOwnPropertySymbols(e);
    r && (o = o.filter(function(r2) {
      return Object.getOwnPropertyDescriptor(e, r2).enumerable;
    })), t.push.apply(t, o);
  }
  return t;
}
__name(ownKeys$1, "ownKeys$1");
function _objectSpread$1(e) {
  for (var r = 1; r < arguments.length; r++) {
    var t = null != arguments[r] ? arguments[r] : {};
    r % 2 ? ownKeys$1(Object(t), true).forEach(function(r2) {
      _defineProperty$2(e, r2, t[r2]);
    }) : Object.getOwnPropertyDescriptors ? Object.defineProperties(e, Object.getOwnPropertyDescriptors(t)) : ownKeys$1(Object(t)).forEach(function(r2) {
      Object.defineProperty(e, r2, Object.getOwnPropertyDescriptor(t, r2));
    });
  }
  return e;
}
__name(_objectSpread$1, "_objectSpread$1");
function _defineProperty$2(e, r, t) {
  return (r = _toPropertyKey$2(r)) in e ? Object.defineProperty(e, r, { value: t, enumerable: true, configurable: true, writable: true }) : e[r] = t, e;
}
__name(_defineProperty$2, "_defineProperty$2");
function _toPropertyKey$2(t) {
  var i = _toPrimitive$2(t, "string");
  return "symbol" == _typeof$2(i) ? i : i + "";
}
__name(_toPropertyKey$2, "_toPropertyKey$2");
function _toPrimitive$2(t, r) {
  if ("object" != _typeof$2(t) || !t) return t;
  var e = t[Symbol.toPrimitive];
  if (void 0 !== e) {
    var i = e.call(t, r);
    if ("object" != _typeof$2(i)) return i;
    throw new TypeError("@@toPrimitive must return a primitive value.");
  }
  return ("string" === r ? String : Number)(t);
}
__name(_toPrimitive$2, "_toPrimitive$2");
var _hoisted_1$1 = ["data-p"];
var _hoisted_2$1 = ["data-p"];
var _hoisted_3 = ["data-p"];
var _hoisted_4 = ["data-p"];
var _hoisted_5 = ["aria-label", "data-p"];
function render$1(_ctx, _cache, $props, $setup, $data, $options) {
  var _directive_ripple = resolveDirective("ripple");
  return openBlock(), createElementBlock("div", mergeProps({
    "class": [_ctx.cx("message"), $props.message.styleClass],
    role: "alert",
    "aria-live": "assertive",
    "aria-atomic": "true",
    "data-p": $options.dataP
  }, _ctx.ptm("message"), {
    onClick: _cache[1] || (_cache[1] = function() {
      return $options.onMessageClick && $options.onMessageClick.apply($options, arguments);
    }),
    onMouseenter: _cache[2] || (_cache[2] = function() {
      return $options.onMouseEnter && $options.onMouseEnter.apply($options, arguments);
    }),
    onMouseleave: _cache[3] || (_cache[3] = function() {
      return $options.onMouseLeave && $options.onMouseLeave.apply($options, arguments);
    })
  }), [$props.templates.container ? (openBlock(), createBlock(resolveDynamicComponent($props.templates.container), {
    key: 0,
    message: $props.message,
    closeCallback: $options.onCloseClick
  }, null, 8, ["message", "closeCallback"])) : (openBlock(), createElementBlock("div", mergeProps({
    key: 1,
    "class": [_ctx.cx("messageContent"), $props.message.contentStyleClass]
  }, _ctx.ptm("messageContent")), [!$props.templates.message ? (openBlock(), createElementBlock(Fragment, {
    key: 0
  }, [(openBlock(), createBlock(resolveDynamicComponent($props.templates.messageicon ? $props.templates.messageicon : $props.templates.icon ? $props.templates.icon : $options.iconComponent && $options.iconComponent.name ? $options.iconComponent : "span"), mergeProps({
    "class": _ctx.cx("messageIcon")
  }, _ctx.ptm("messageIcon")), null, 16, ["class"])), createBaseVNode("div", mergeProps({
    "class": _ctx.cx("messageText"),
    "data-p": $options.dataP
  }, _ctx.ptm("messageText")), [createBaseVNode("span", mergeProps({
    "class": _ctx.cx("summary"),
    "data-p": $options.dataP
  }, _ctx.ptm("summary")), toDisplayString($props.message.summary), 17, _hoisted_3), $props.message.detail ? (openBlock(), createElementBlock("div", mergeProps({
    key: 0,
    "class": _ctx.cx("detail"),
    "data-p": $options.dataP
  }, _ctx.ptm("detail")), toDisplayString($props.message.detail), 17, _hoisted_4)) : createCommentVNode("", true)], 16, _hoisted_2$1)], 64)) : (openBlock(), createBlock(resolveDynamicComponent($props.templates.message), {
    key: 1,
    message: $props.message
  }, null, 8, ["message"])), $props.message.closable !== false ? (openBlock(), createElementBlock("div", normalizeProps(mergeProps({
    key: 2
  }, _ctx.ptm("buttonContainer"))), [withDirectives((openBlock(), createElementBlock("button", mergeProps({
    "class": _ctx.cx("closeButton"),
    type: "button",
    "aria-label": $options.closeAriaLabel,
    onClick: _cache[0] || (_cache[0] = function() {
      return $options.onCloseClick && $options.onCloseClick.apply($options, arguments);
    }),
    autofocus: "",
    "data-p": $options.dataP
  }, _objectSpread$1(_objectSpread$1({}, $props.closeButtonProps), _ctx.ptm("closeButton"))), [(openBlock(), createBlock(resolveDynamicComponent($props.templates.closeicon || "TimesIcon"), mergeProps({
    "class": [_ctx.cx("closeIcon"), $props.closeIcon]
  }, _ctx.ptm("closeIcon")), null, 16, ["class"]))], 16, _hoisted_5)), [[_directive_ripple]])], 16)) : createCommentVNode("", true)], 16))], 16, _hoisted_1$1);
}
__name(render$1, "render$1");
script$1$1.render = render$1;
function _typeof$1(o) {
  "@babel/helpers - typeof";
  return _typeof$1 = "function" == typeof Symbol && "symbol" == typeof Symbol.iterator ? function(o2) {
    return typeof o2;
  } : function(o2) {
    return o2 && "function" == typeof Symbol && o2.constructor === Symbol && o2 !== Symbol.prototype ? "symbol" : typeof o2;
  }, _typeof$1(o);
}
__name(_typeof$1, "_typeof$1");
function _defineProperty$1(e, r, t) {
  return (r = _toPropertyKey$1(r)) in e ? Object.defineProperty(e, r, { value: t, enumerable: true, configurable: true, writable: true }) : e[r] = t, e;
}
__name(_defineProperty$1, "_defineProperty$1");
function _toPropertyKey$1(t) {
  var i = _toPrimitive$1(t, "string");
  return "symbol" == _typeof$1(i) ? i : i + "";
}
__name(_toPropertyKey$1, "_toPropertyKey$1");
function _toPrimitive$1(t, r) {
  if ("object" != _typeof$1(t) || !t) return t;
  var e = t[Symbol.toPrimitive];
  if (void 0 !== e) {
    var i = e.call(t, r);
    if ("object" != _typeof$1(i)) return i;
    throw new TypeError("@@toPrimitive must return a primitive value.");
  }
  return ("string" === r ? String : Number)(t);
}
__name(_toPrimitive$1, "_toPrimitive$1");
function _toConsumableArray(r) {
  return _arrayWithoutHoles(r) || _iterableToArray(r) || _unsupportedIterableToArray(r) || _nonIterableSpread();
}
__name(_toConsumableArray, "_toConsumableArray");
function _nonIterableSpread() {
  throw new TypeError("Invalid attempt to spread non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.");
}
__name(_nonIterableSpread, "_nonIterableSpread");
function _unsupportedIterableToArray(r, a) {
  if (r) {
    if ("string" == typeof r) return _arrayLikeToArray(r, a);
    var t = {}.toString.call(r).slice(8, -1);
    return "Object" === t && r.constructor && (t = r.constructor.name), "Map" === t || "Set" === t ? Array.from(r) : "Arguments" === t || /^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(t) ? _arrayLikeToArray(r, a) : void 0;
  }
}
__name(_unsupportedIterableToArray, "_unsupportedIterableToArray");
function _iterableToArray(r) {
  if ("undefined" != typeof Symbol && null != r[Symbol.iterator] || null != r["@@iterator"]) return Array.from(r);
}
__name(_iterableToArray, "_iterableToArray");
function _arrayWithoutHoles(r) {
  if (Array.isArray(r)) return _arrayLikeToArray(r);
}
__name(_arrayWithoutHoles, "_arrayWithoutHoles");
function _arrayLikeToArray(r, a) {
  (null == a || a > r.length) && (a = r.length);
  for (var e = 0, n = Array(a); e < a; e++) n[e] = r[e];
  return n;
}
__name(_arrayLikeToArray, "_arrayLikeToArray");
var messageIdx = 0;
var script$3 = {
  name: "Toast",
  "extends": script$2,
  inheritAttrs: false,
  emits: ["close", "life-end"],
  data: /* @__PURE__ */ __name(function data() {
    return {
      messages: []
    };
  }, "data"),
  styleElement: null,
  mounted: /* @__PURE__ */ __name(function mounted2() {
    ToastEventBus.on("add", this.onAdd);
    ToastEventBus.on("remove", this.onRemove);
    ToastEventBus.on("remove-group", this.onRemoveGroup);
    ToastEventBus.on("remove-all-groups", this.onRemoveAllGroups);
    if (this.breakpoints) {
      this.createStyle();
    }
  }, "mounted"),
  beforeUnmount: /* @__PURE__ */ __name(function beforeUnmount2() {
    this.destroyStyle();
    if (this.$refs.container && this.autoZIndex) {
      ZIndex.clear(this.$refs.container);
    }
    ToastEventBus.off("add", this.onAdd);
    ToastEventBus.off("remove", this.onRemove);
    ToastEventBus.off("remove-group", this.onRemoveGroup);
    ToastEventBus.off("remove-all-groups", this.onRemoveAllGroups);
  }, "beforeUnmount"),
  methods: {
    add: /* @__PURE__ */ __name(function add(message2) {
      if (message2.id == null) {
        message2.id = messageIdx++;
      }
      this.messages = [].concat(_toConsumableArray(this.messages), [message2]);
    }, "add"),
    remove: /* @__PURE__ */ __name(function remove(params) {
      var index = this.messages.findIndex(function(m) {
        return m.id === params.message.id;
      });
      if (index !== -1) {
        this.messages.splice(index, 1);
        this.$emit(params.type, {
          message: params.message
        });
      }
    }, "remove"),
    onAdd: /* @__PURE__ */ __name(function onAdd(message2) {
      if (this.group == message2.group) {
        this.add(message2);
      }
    }, "onAdd"),
    onRemove: /* @__PURE__ */ __name(function onRemove(message2) {
      this.remove({
        message: message2,
        type: "close"
      });
    }, "onRemove"),
    onRemoveGroup: /* @__PURE__ */ __name(function onRemoveGroup(group) {
      if (this.group === group) {
        this.messages = [];
      }
    }, "onRemoveGroup"),
    onRemoveAllGroups: /* @__PURE__ */ __name(function onRemoveAllGroups() {
      var _this = this;
      this.messages.forEach(function(message2) {
        return _this.$emit("close", {
          message: message2
        });
      });
      this.messages = [];
    }, "onRemoveAllGroups"),
    onEnter: /* @__PURE__ */ __name(function onEnter() {
      if (this.autoZIndex) {
        ZIndex.set("modal", this.$refs.container, this.baseZIndex || this.$primevue.config.zIndex.modal);
      }
    }, "onEnter"),
    onLeave: /* @__PURE__ */ __name(function onLeave() {
      var _this2 = this;
      if (this.$refs.container && this.autoZIndex && isEmpty(this.messages)) {
        setTimeout(function() {
          ZIndex.clear(_this2.$refs.container);
        }, 200);
      }
    }, "onLeave"),
    createStyle: /* @__PURE__ */ __name(function createStyle() {
      if (!this.styleElement && !this.isUnstyled) {
        var _this$$primevue;
        this.styleElement = document.createElement("style");
        this.styleElement.type = "text/css";
        setAttribute(this.styleElement, "nonce", (_this$$primevue = this.$primevue) === null || _this$$primevue === void 0 || (_this$$primevue = _this$$primevue.config) === null || _this$$primevue === void 0 || (_this$$primevue = _this$$primevue.csp) === null || _this$$primevue === void 0 ? void 0 : _this$$primevue.nonce);
        document.head.appendChild(this.styleElement);
        var innerHTML = "";
        for (var breakpoint in this.breakpoints) {
          var breakpointStyle = "";
          for (var styleProp in this.breakpoints[breakpoint]) {
            breakpointStyle += styleProp + ":" + this.breakpoints[breakpoint][styleProp] + "!important;";
          }
          innerHTML += "\n                        @media screen and (max-width: ".concat(breakpoint, ") {\n                            .p-toast[").concat(this.$attrSelector, "] {\n                                ").concat(breakpointStyle, "\n                            }\n                        }\n                    ");
        }
        this.styleElement.innerHTML = innerHTML;
      }
    }, "createStyle"),
    destroyStyle: /* @__PURE__ */ __name(function destroyStyle() {
      if (this.styleElement) {
        document.head.removeChild(this.styleElement);
        this.styleElement = null;
      }
    }, "destroyStyle")
  },
  computed: {
    dataP: /* @__PURE__ */ __name(function dataP2() {
      return cn(_defineProperty$1({}, this.position, this.position));
    }, "dataP")
  },
  components: {
    ToastMessage: script$1$1,
    Portal: script$7
  }
};
function _typeof$4(o) {
  "@babel/helpers - typeof";
  return _typeof$4 = "function" == typeof Symbol && "symbol" == typeof Symbol.iterator ? function(o2) {
    return typeof o2;
  } : function(o2) {
    return o2 && "function" == typeof Symbol && o2.constructor === Symbol && o2 !== Symbol.prototype ? "symbol" : typeof o2;
  }, _typeof$4(o);
}
__name(_typeof$4, "_typeof$4");
function ownKeys(e, r) {
  var t = Object.keys(e);
  if (Object.getOwnPropertySymbols) {
    var o = Object.getOwnPropertySymbols(e);
    r && (o = o.filter(function(r2) {
      return Object.getOwnPropertyDescriptor(e, r2).enumerable;
    })), t.push.apply(t, o);
  }
  return t;
}
__name(ownKeys, "ownKeys");
function _objectSpread(e) {
  for (var r = 1; r < arguments.length; r++) {
    var t = null != arguments[r] ? arguments[r] : {};
    r % 2 ? ownKeys(Object(t), true).forEach(function(r2) {
      _defineProperty$4(e, r2, t[r2]);
    }) : Object.getOwnPropertyDescriptors ? Object.defineProperties(e, Object.getOwnPropertyDescriptors(t)) : ownKeys(Object(t)).forEach(function(r2) {
      Object.defineProperty(e, r2, Object.getOwnPropertyDescriptor(t, r2));
    });
  }
  return e;
}
__name(_objectSpread, "_objectSpread");
function _defineProperty$4(e, r, t) {
  return (r = _toPropertyKey$4(r)) in e ? Object.defineProperty(e, r, { value: t, enumerable: true, configurable: true, writable: true }) : e[r] = t, e;
}
__name(_defineProperty$4, "_defineProperty$4");
function _toPropertyKey$4(t) {
  var i = _toPrimitive$4(t, "string");
  return "symbol" == _typeof$4(i) ? i : i + "";
}
__name(_toPropertyKey$4, "_toPropertyKey$4");
function _toPrimitive$4(t, r) {
  if ("object" != _typeof$4(t) || !t) return t;
  var e = t[Symbol.toPrimitive];
  if (void 0 !== e) {
    var i = e.call(t, r);
    if ("object" != _typeof$4(i)) return i;
    throw new TypeError("@@toPrimitive must return a primitive value.");
  }
  return ("string" === r ? String : Number)(t);
}
__name(_toPrimitive$4, "_toPrimitive$4");
var _hoisted_1$2 = ["data-p"];
function render$2(_ctx, _cache, $props, $setup, $data, $options) {
  var _component_ToastMessage = resolveComponent("ToastMessage");
  var _component_Portal = resolveComponent("Portal");
  return openBlock(), createBlock(_component_Portal, null, {
    "default": withCtx(function() {
      return [createBaseVNode("div", mergeProps({
        ref: "container",
        "class": _ctx.cx("root"),
        style: _ctx.sx("root", true, {
          position: _ctx.position
        }),
        "data-p": $options.dataP
      }, _ctx.ptmi("root")), [createVNode(TransitionGroup, mergeProps({
        name: "p-toast-message",
        tag: "div",
        onEnter: $options.onEnter,
        onLeave: $options.onLeave
      }, _objectSpread({}, _ctx.ptm("transition"))), {
        "default": withCtx(function() {
          return [(openBlock(true), createElementBlock(Fragment, null, renderList($data.messages, function(msg) {
            return openBlock(), createBlock(_component_ToastMessage, {
              key: msg.id,
              message: msg,
              templates: _ctx.$slots,
              closeIcon: _ctx.closeIcon,
              infoIcon: _ctx.infoIcon,
              warnIcon: _ctx.warnIcon,
              errorIcon: _ctx.errorIcon,
              successIcon: _ctx.successIcon,
              closeButtonProps: _ctx.closeButtonProps,
              unstyled: _ctx.unstyled,
              onClose: _cache[0] || (_cache[0] = function($event) {
                return $options.remove($event);
              }),
              pt: _ctx.pt
            }, null, 8, ["message", "templates", "closeIcon", "infoIcon", "warnIcon", "errorIcon", "successIcon", "closeButtonProps", "unstyled", "pt"]);
          }), 128))];
        }),
        _: 1
      }, 16, ["onEnter", "onLeave"])], 16, _hoisted_1$2)];
    }),
    _: 1
  });
}
__name(render$2, "render$2");
script$3.render = render$2;
var style = /* @__PURE__ */ __name(({ dt: r }) => `
.p-drawer {
    display: flex;
    flex-direction: column;
    transform: translate3d(0px, 0px, 0px);
    position: relative;
    transition: transform 0.3s;
    background: ${r("drawer.background")};
    color: ${r("drawer.color")};
    border: 1px solid ${r("drawer.border.color")};
    box-shadow: ${r("drawer.shadow")};
}

.p-drawer-content {
    overflow-y: auto;
    flex-grow: 1;
    padding: ${r("drawer.content.padding")};
}

.p-drawer-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    flex-shrink: 0;
    padding: ${r("drawer.header.padding")};
}

.p-drawer-footer {
    padding: ${r("drawer.footer.padding")};
}

.p-drawer-title {
    font-weight: ${r("drawer.title.font.weight")};
    font-size: ${r("drawer.title.font.size")};
}

.p-drawer-full .p-drawer {
    transition: none;
    transform: none;
    width: 100vw !important;
    height: 100vh !important;
    max-height: 100%;
    top: 0px !important;
    left: 0px !important;
    border-width: 1px;
}

.p-drawer-left .p-drawer-enter-from,
.p-drawer-left .p-drawer-leave-to {
    transform: translateX(-100%);
}

.p-drawer-right .p-drawer-enter-from,
.p-drawer-right .p-drawer-leave-to {
    transform: translateX(100%);
}

.p-drawer-top .p-drawer-enter-from,
.p-drawer-top .p-drawer-leave-to {
    transform: translateY(-100%);
}

.p-drawer-bottom .p-drawer-enter-from,
.p-drawer-bottom .p-drawer-leave-to {
    transform: translateY(100%);
}

.p-drawer-full .p-drawer-enter-from,
.p-drawer-full .p-drawer-leave-to {
    opacity: 0;
}

.p-drawer-full .p-drawer-enter-active,
.p-drawer-full .p-drawer-leave-active {
    transition: opacity 400ms cubic-bezier(0.25, 0.8, 0.25, 1);
}

.p-drawer-left .p-drawer {
    width: 20rem;
    height: 100%;
    border-inline-end-width: 1px;
}

.p-drawer-right .p-drawer {
    width: 20rem;
    height: 100%;
    border-inline-start-width: 1px;
}

.p-drawer-top .p-drawer {
    height: 10rem;
    width: 100%;
    border-block-end-width: 1px;
}

.p-drawer-bottom .p-drawer {
    height: 10rem;
    width: 100%;
    border-block-start-width: 1px;
}

.p-drawer-left .p-drawer-content,
.p-drawer-right .p-drawer-content,
.p-drawer-top .p-drawer-content,
.p-drawer-bottom .p-drawer-content {
    width: 100%;
    height: 100%;
}

.p-drawer-open {
    display: flex;
}

.p-drawer-mask:dir(rtl) {
    flex-direction: row-reverse;
}
`, "style");
var inlineStyles = {
  mask: /* @__PURE__ */ __name(function mask(_ref) {
    var position = _ref.position, modal = _ref.modal;
    return {
      position: "fixed",
      height: "100%",
      width: "100%",
      left: 0,
      top: 0,
      display: "flex",
      justifyContent: position === "left" ? "flex-start" : position === "right" ? "flex-end" : "center",
      alignItems: position === "top" ? "flex-start" : position === "bottom" ? "flex-end" : "center",
      pointerEvents: modal ? "auto" : "none"
    };
  }, "mask"),
  root: {
    pointerEvents: "auto"
  }
};
var classes = {
  mask: /* @__PURE__ */ __name(function mask2(_ref2) {
    var instance = _ref2.instance, props = _ref2.props;
    var positions = ["left", "right", "top", "bottom"];
    var pos = positions.find(function(item) {
      return item === props.position;
    });
    return ["p-drawer-mask", {
      "p-overlay-mask p-overlay-mask-enter": props.modal,
      "p-drawer-open": instance.containerVisible,
      "p-drawer-full": instance.fullScreen
    }, pos ? "p-drawer-".concat(pos) : ""];
  }, "mask"),
  root: /* @__PURE__ */ __name(function root3(_ref3) {
    var instance = _ref3.instance;
    return ["p-drawer p-component", {
      "p-drawer-full": instance.fullScreen
    }];
  }, "root"),
  header: "p-drawer-header",
  title: "p-drawer-title",
  pcCloseButton: "p-drawer-close-button",
  content: "p-drawer-content",
  footer: "p-drawer-footer"
};
var DrawerStyle = BaseStyle.extend({
  name: "drawer",
  style,
  classes,
  inlineStyles
});
var script$1 = {
  name: "BaseDrawer",
  "extends": script$b,
  props: {
    visible: {
      type: Boolean,
      "default": false
    },
    position: {
      type: String,
      "default": "left"
    },
    header: {
      type: null,
      "default": null
    },
    baseZIndex: {
      type: Number,
      "default": 0
    },
    autoZIndex: {
      type: Boolean,
      "default": true
    },
    dismissable: {
      type: Boolean,
      "default": true
    },
    showCloseIcon: {
      type: Boolean,
      "default": true
    },
    closeButtonProps: {
      type: Object,
      "default": /* @__PURE__ */ __name(function _default() {
        return {
          severity: "secondary",
          text: true,
          rounded: true
        };
      }, "_default")
    },
    closeIcon: {
      type: String,
      "default": void 0
    },
    modal: {
      type: Boolean,
      "default": true
    },
    blockScroll: {
      type: Boolean,
      "default": false
    }
  },
  style: DrawerStyle,
  provide: /* @__PURE__ */ __name(function provide2() {
    return {
      $pcDrawer: this,
      $parentInstance: this
    };
  }, "provide")
};
function _typeof(o) {
  "@babel/helpers - typeof";
  return _typeof = "function" == typeof Symbol && "symbol" == typeof Symbol.iterator ? function(o2) {
    return typeof o2;
  } : function(o2) {
    return o2 && "function" == typeof Symbol && o2.constructor === Symbol && o2 !== Symbol.prototype ? "symbol" : typeof o2;
  }, _typeof(o);
}
__name(_typeof, "_typeof");
function _defineProperty(e, r, t) {
  return (r = _toPropertyKey(r)) in e ? Object.defineProperty(e, r, { value: t, enumerable: true, configurable: true, writable: true }) : e[r] = t, e;
}
__name(_defineProperty, "_defineProperty");
function _toPropertyKey(t) {
  var i = _toPrimitive(t, "string");
  return "symbol" == _typeof(i) ? i : i + "";
}
__name(_toPropertyKey, "_toPropertyKey");
function _toPrimitive(t, r) {
  if ("object" != _typeof(t) || !t) return t;
  var e = t[Symbol.toPrimitive];
  if (void 0 !== e) {
    var i = e.call(t, r);
    if ("object" != _typeof(i)) return i;
    throw new TypeError("@@toPrimitive must return a primitive value.");
  }
  return ("string" === r ? String : Number)(t);
}
__name(_toPrimitive, "_toPrimitive");
var script = {
  name: "Drawer",
  "extends": script$1,
  inheritAttrs: false,
  emits: ["update:visible", "show", "after-show", "hide", "after-hide", "before-hide"],
  data: /* @__PURE__ */ __name(function data2() {
    return {
      containerVisible: this.visible
    };
  }, "data"),
  container: null,
  mask: null,
  content: null,
  headerContainer: null,
  footerContainer: null,
  closeButton: null,
  outsideClickListener: null,
  documentKeydownListener: null,
  watch: {
    dismissable: /* @__PURE__ */ __name(function dismissable(newValue) {
      if (newValue) {
        this.enableDocumentSettings();
      } else {
        this.disableDocumentSettings();
      }
    }, "dismissable")
  },
  updated: /* @__PURE__ */ __name(function updated() {
    if (this.visible) {
      this.containerVisible = this.visible;
    }
  }, "updated"),
  beforeUnmount: /* @__PURE__ */ __name(function beforeUnmount3() {
    this.disableDocumentSettings();
    if (this.mask && this.autoZIndex) {
      ZIndex.clear(this.mask);
    }
    this.container = null;
    this.mask = null;
  }, "beforeUnmount"),
  methods: {
    hide: /* @__PURE__ */ __name(function hide() {
      this.$emit("update:visible", false);
    }, "hide"),
    onEnter: /* @__PURE__ */ __name(function onEnter2() {
      this.$emit("show");
      this.focus();
      this.bindDocumentKeyDownListener();
      if (this.autoZIndex) {
        ZIndex.set("modal", this.mask, this.baseZIndex || this.$primevue.config.zIndex.modal);
      }
    }, "onEnter"),
    onAfterEnter: /* @__PURE__ */ __name(function onAfterEnter() {
      this.enableDocumentSettings();
      this.$emit("after-show");
    }, "onAfterEnter"),
    onBeforeLeave: /* @__PURE__ */ __name(function onBeforeLeave() {
      if (this.modal) {
        !this.isUnstyled && addClass(this.mask, "p-overlay-mask-leave");
      }
      this.$emit("before-hide");
    }, "onBeforeLeave"),
    onLeave: /* @__PURE__ */ __name(function onLeave2() {
      this.$emit("hide");
    }, "onLeave"),
    onAfterLeave: /* @__PURE__ */ __name(function onAfterLeave() {
      if (this.autoZIndex) {
        ZIndex.clear(this.mask);
      }
      this.unbindDocumentKeyDownListener();
      this.containerVisible = false;
      this.disableDocumentSettings();
      this.$emit("after-hide");
    }, "onAfterLeave"),
    onMaskClick: /* @__PURE__ */ __name(function onMaskClick(event) {
      if (this.dismissable && this.modal && this.mask === event.target) {
        this.hide();
      }
    }, "onMaskClick"),
    focus: /* @__PURE__ */ __name(function focus$1() {
      var findFocusableElement = /* @__PURE__ */ __name(function findFocusableElement2(container) {
        return container && container.querySelector("[autofocus]");
      }, "findFocusableElement");
      var focusTarget = this.$slots.header && findFocusableElement(this.headerContainer);
      if (!focusTarget) {
        focusTarget = this.$slots["default"] && findFocusableElement(this.container);
        if (!focusTarget) {
          focusTarget = this.$slots.footer && findFocusableElement(this.footerContainer);
          if (!focusTarget) {
            focusTarget = this.closeButton;
          }
        }
      }
      focusTarget && focus(focusTarget);
    }, "focus$1"),
    enableDocumentSettings: /* @__PURE__ */ __name(function enableDocumentSettings() {
      if (this.dismissable && !this.modal) {
        this.bindOutsideClickListener();
      }
      if (this.blockScroll) {
        blockBodyScroll();
      }
    }, "enableDocumentSettings"),
    disableDocumentSettings: /* @__PURE__ */ __name(function disableDocumentSettings() {
      this.unbindOutsideClickListener();
      if (this.blockScroll) {
        unblockBodyScroll();
      }
    }, "disableDocumentSettings"),
    onKeydown: /* @__PURE__ */ __name(function onKeydown(event) {
      if (event.code === "Escape") {
        this.hide();
      }
    }, "onKeydown"),
    containerRef: /* @__PURE__ */ __name(function containerRef(el) {
      this.container = el;
    }, "containerRef"),
    maskRef: /* @__PURE__ */ __name(function maskRef(el) {
      this.mask = el;
    }, "maskRef"),
    contentRef: /* @__PURE__ */ __name(function contentRef(el) {
      this.content = el;
    }, "contentRef"),
    headerContainerRef: /* @__PURE__ */ __name(function headerContainerRef(el) {
      this.headerContainer = el;
    }, "headerContainerRef"),
    footerContainerRef: /* @__PURE__ */ __name(function footerContainerRef(el) {
      this.footerContainer = el;
    }, "footerContainerRef"),
    closeButtonRef: /* @__PURE__ */ __name(function closeButtonRef(el) {
      this.closeButton = el ? el.$el : void 0;
    }, "closeButtonRef"),
    bindDocumentKeyDownListener: /* @__PURE__ */ __name(function bindDocumentKeyDownListener() {
      if (!this.documentKeydownListener) {
        this.documentKeydownListener = this.onKeydown;
        document.addEventListener("keydown", this.documentKeydownListener);
      }
    }, "bindDocumentKeyDownListener"),
    unbindDocumentKeyDownListener: /* @__PURE__ */ __name(function unbindDocumentKeyDownListener() {
      if (this.documentKeydownListener) {
        document.removeEventListener("keydown", this.documentKeydownListener);
        this.documentKeydownListener = null;
      }
    }, "unbindDocumentKeyDownListener"),
    bindOutsideClickListener: /* @__PURE__ */ __name(function bindOutsideClickListener() {
      var _this = this;
      if (!this.outsideClickListener) {
        this.outsideClickListener = function(event) {
          if (_this.isOutsideClicked(event)) {
            _this.hide();
          }
        };
        document.addEventListener("click", this.outsideClickListener, true);
      }
    }, "bindOutsideClickListener"),
    unbindOutsideClickListener: /* @__PURE__ */ __name(function unbindOutsideClickListener() {
      if (this.outsideClickListener) {
        document.removeEventListener("click", this.outsideClickListener, true);
        this.outsideClickListener = null;
      }
    }, "unbindOutsideClickListener"),
    isOutsideClicked: /* @__PURE__ */ __name(function isOutsideClicked(event) {
      return this.container && !this.container.contains(event.target);
    }, "isOutsideClicked")
  },
  computed: {
    fullScreen: /* @__PURE__ */ __name(function fullScreen() {
      return this.position === "full";
    }, "fullScreen"),
    closeAriaLabel: /* @__PURE__ */ __name(function closeAriaLabel2() {
      return this.$primevue.config.locale.aria ? this.$primevue.config.locale.aria.close : void 0;
    }, "closeAriaLabel"),
    dataP: /* @__PURE__ */ __name(function dataP3() {
      return cn(_defineProperty(_defineProperty(_defineProperty({
        "full-screen": this.position === "full"
      }, this.position, this.position), "open", this.containerVisible), "modal", this.modal));
    }, "dataP")
  },
  directives: {
    focustrap: FocusTrap
  },
  components: {
    Button: script$c,
    Portal: script$7,
    TimesIcon: script$a
  }
};
var _hoisted_1 = ["data-p"];
var _hoisted_2 = ["aria-modal", "data-p"];
function render(_ctx, _cache, $props, $setup, $data, $options) {
  var _component_Button = resolveComponent("Button");
  var _component_Portal = resolveComponent("Portal");
  var _directive_focustrap = resolveDirective("focustrap");
  return openBlock(), createBlock(_component_Portal, null, {
    "default": withCtx(function() {
      return [$data.containerVisible ? (openBlock(), createElementBlock("div", mergeProps({
        key: 0,
        ref: $options.maskRef,
        onMousedown: _cache[0] || (_cache[0] = function() {
          return $options.onMaskClick && $options.onMaskClick.apply($options, arguments);
        }),
        "class": _ctx.cx("mask"),
        style: _ctx.sx("mask", true, {
          position: _ctx.position,
          modal: _ctx.modal
        }),
        "data-p": $options.dataP
      }, _ctx.ptm("mask")), [createVNode(Transition, mergeProps({
        name: "p-drawer",
        onEnter: $options.onEnter,
        onAfterEnter: $options.onAfterEnter,
        onBeforeLeave: $options.onBeforeLeave,
        onLeave: $options.onLeave,
        onAfterLeave: $options.onAfterLeave,
        appear: ""
      }, _ctx.ptm("transition")), {
        "default": withCtx(function() {
          return [_ctx.visible ? withDirectives((openBlock(), createElementBlock("div", mergeProps({
            key: 0,
            ref: $options.containerRef,
            "class": _ctx.cx("root"),
            style: _ctx.sx("root"),
            role: "complementary",
            "aria-modal": _ctx.modal,
            "data-p": $options.dataP
          }, _ctx.ptmi("root")), [_ctx.$slots.container ? renderSlot(_ctx.$slots, "container", {
            key: 0,
            closeCallback: $options.hide
          }) : (openBlock(), createElementBlock(Fragment, {
            key: 1
          }, [createBaseVNode("div", mergeProps({
            ref: $options.headerContainerRef,
            "class": _ctx.cx("header")
          }, _ctx.ptm("header")), [renderSlot(_ctx.$slots, "header", {
            "class": normalizeClass(_ctx.cx("title"))
          }, function() {
            return [_ctx.header ? (openBlock(), createElementBlock("div", mergeProps({
              key: 0,
              "class": _ctx.cx("title")
            }, _ctx.ptm("title")), toDisplayString(_ctx.header), 17)) : createCommentVNode("", true)];
          }), _ctx.showCloseIcon ? renderSlot(_ctx.$slots, "closebutton", {
            key: 0,
            closeCallback: $options.hide
          }, function() {
            return [createVNode(_component_Button, mergeProps({
              ref: $options.closeButtonRef,
              type: "button",
              "class": _ctx.cx("pcCloseButton"),
              "aria-label": $options.closeAriaLabel,
              unstyled: _ctx.unstyled,
              onClick: $options.hide
            }, _ctx.closeButtonProps, {
              pt: _ctx.ptm("pcCloseButton"),
              "data-pc-group-section": "iconcontainer"
            }), {
              icon: withCtx(function(slotProps) {
                return [renderSlot(_ctx.$slots, "closeicon", {}, function() {
                  return [(openBlock(), createBlock(resolveDynamicComponent(_ctx.closeIcon ? "span" : "TimesIcon"), mergeProps({
                    "class": [_ctx.closeIcon, slotProps["class"]]
                  }, _ctx.ptm("pcCloseButton")["icon"]), null, 16, ["class"]))];
                })];
              }),
              _: 3
            }, 16, ["class", "aria-label", "unstyled", "onClick", "pt"])];
          }) : createCommentVNode("", true)], 16), createBaseVNode("div", mergeProps({
            ref: $options.contentRef,
            "class": _ctx.cx("content")
          }, _ctx.ptm("content")), [renderSlot(_ctx.$slots, "default")], 16), _ctx.$slots.footer ? (openBlock(), createElementBlock("div", mergeProps({
            key: 0,
            ref: $options.footerContainerRef,
            "class": _ctx.cx("footer")
          }, _ctx.ptm("footer")), [renderSlot(_ctx.$slots, "footer")], 16)) : createCommentVNode("", true)], 64))], 16, _hoisted_2)), [[_directive_focustrap]]) : createCommentVNode("", true)];
        }),
        _: 3
      }, 16, ["onEnter", "onAfterEnter", "onBeforeLeave", "onLeave", "onAfterLeave"])], 16, _hoisted_1)) : createCommentVNode("", true)];
    }),
    _: 3
  });
}
__name(render, "render");
script.render = render;
export {
  script as a,
  script$5 as b,
  script$4 as c,
  script$3 as s
};
//# sourceMappingURL=index-DkI-wNAU.js.map
