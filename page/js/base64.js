(function () { "use strict";
  function encodeBytes(bytes) { if (!(bytes instanceof Uint8Array)) bytes = new Uint8Array(bytes); let binary = ""; const chunkSize = 0x8000; for (let offset = 0; offset < bytes.length; offset += chunkSize) binary += String.fromCharCode(...bytes.subarray(offset, offset + chunkSize)); return btoa(binary); }
  function decodeBytes(base64) { const binary = atob(String(base64).replace(/\s/g, "")), bytes = new Uint8Array(binary.length); for (let index = 0; index < binary.length; index += 1) bytes[index] = binary.charCodeAt(index); return bytes; }
  function encodeText(text) { return encodeBytes(new TextEncoder().encode(String(text))); } function decodeText(base64) { return new TextDecoder("utf-8", { fatal: true }).decode(decodeBytes(base64)); }
  window.RtGBase64 = { encodeText, decodeText, encodeBytes, decodeBytes };
}());
