HTMLCollection.prototype.forEach = Array.prototype.forEach;

"use strict";
var Passkeys = (() => {

	var __defProp = Object.defineProperty;
	var __getOwnPropDesc = Object.getOwnPropertyDescriptor;
	var __getOwnPropNames = Object.getOwnPropertyNames;
	var __hasOwnProp = Object.prototype.hasOwnProperty;

	var __export = (target, all) => {
		for (var name in all)
			__defProp(target, name, { get: all[name], enumerable: true });
	};
	var __copyProps = (to, from, except, desc) => {
		if (from && typeof from === "object" || typeof from === "function") {
			for (let key of __getOwnPropNames(from))
				if (!__hasOwnProp.call(to, key) && key !== except)
					__defProp(to, key, { get: () => from[key], enumerable: !(desc = __getOwnPropDesc(from, key)) || desc.enumerable });
		}
		return to;
	};
	var __toCommonJS = (mod2) => __copyProps(__defProp({}, "__esModule", { value: true }), mod2);
	var input_exports = {};

	class Passkeys {

		constructor(power = 128, ...args){
			document.addEventListener("DOMContentLoaded", function(event) {
				console.log('Passkeys.')
			}.bind(this));
		}

		// register / create a new credential
		async register() {
			window.relock.request('/relock/register', {id: null})
				.then((response) => response.json())
				.then((options) => {
					// Registration args object
					let args = {
						publicKey: {
								rp: {
									id: options.rp.id,
									name: options.rp.name
								},
								authenticatorSelection: options.authenticatorSelection,
								user: {
									id: options.user.id.base64url_decode(),
									name: options.user.name,
									displayName: options.user.displayName
								},
								pubKeyCredParams: options.pubKeyCredParams,
								// attestation: options.attestation,
								timeout: parseInt(options.timeout),
								challenge: options.challenge.base64url_decode()
						}
					};

					navigator.credentials.create(args)
						.then((credential) => {
							// convert credential to json serializeable
							const serializeable = {
									authenticatorAttachment: credential.authenticatorAttachment,
									id: credential.id,
									rawId: credential.rawId.base64url_encode(),
									response: {
										attestationObject: credential.response.attestationObject.base64url_encode(),
										clientDataJSON: credential.response.clientDataJSON.base64url_encode()
									},
									type: credential.type
							};
							this.store(serializeable)
						}).catch((err) => {
							console.log("ERROR", err);
						})
				}).catch((error) => {
					console.error('Registration of credential Faild.', error)
				});
		}

		// register / create a new credential
		async store(credential) {
			window.relock.request('/relock/register', {credential: credential})
				.then((response) => response.json())
				.then((json) => {
					document.dispatchEvent(
						new CustomEvent('XPasskeyCreated', {bubbles: true, 
													 		detail:{ id: new Uint8Array(json.id) }}));
				}).catch((error) => {
					console.error('Storage of credential Faild.')
				});
		}

		async authenticate(credential) {
			window.relock.request('/relock/authenticate', {id: credential})
				.then((response) => response.json())
				.then((json) => {
					// Login args object
					const args = {
						publicKey: json,
					};

					if(args.publicKey.allowCredentials.length)
						args.publicKey.allowCredentials[0].id = args.publicKey.allowCredentials[0].id.base64url_decode();
					args.publicKey.challenge = args.publicKey.challenge.base64url_decode()

					return navigator.credentials.get(args)
							.then((credential) => {
								// convert credential to json serializeable
								const serializeable = {
										authenticatorAttachment: credential.authenticatorAttachment,
										id: credential.id,
										rawId: credential.rawId.base64url_encode(),
										response: {
										authenticatorData: credential.response.authenticatorData.base64url_encode(),
												clientDataJSON: credential.response.clientDataJSON.base64url_encode(),
												signature: credential.response.signature.base64url_encode(),
												userHandle: credential.response.userHandle.base64url_encode(),
										},
										type: credential.type
								};

								this.signin(serializeable);
							})
							.catch((err) => {
								console.log("ERROR", err);
							});
				 })
				.catch((error) => {
					console.error(error)
				 });
		}

		async signin(credential) {
			window.relock.request('/relock/authenticate', {credential: credential})
				.then((response) => response.json())
				.then((json) => {
					console.info('User passkey signature is correct.')
					document.dispatchEvent(new CustomEvent('XPasskeyAuthenticated', {bubbles: true, 
													 					  	  		 detail:{ id: new Uint8Array(json.id) }}));
				 })
				.catch((error) => {
					console.error('Registration of credential Faild.')
				 });
		}
	}

	let object = undefined

	try {
		object = new Passkeys()
	}
	catch(err) {
		console.error('Fatal object start.')
	}
	finally{
		if(object){
			__export(input_exports, {
				register:    () => object.register.bind(object),
				authenticate:() => object.authenticate.bind(object),
				public:      () => object.public
			});

			return __toCommonJS(input_exports);
		}
	}
})();

"use strict";
var nobleHashes = (() => {
  var __defProp = Object.defineProperty;
  var __getOwnPropDesc = Object.getOwnPropertyDescriptor;
  var __getOwnPropNames = Object.getOwnPropertyNames;
  var __hasOwnProp = Object.prototype.hasOwnProperty;
  var __export = (target, all) => {
    for (var name in all)
      __defProp(target, name, { get: all[name], enumerable: true });
  };
  var __copyProps = (to, from, except, desc) => {
    if (from && typeof from === "object" || typeof from === "function") {
      for (let key of __getOwnPropNames(from))
        if (!__hasOwnProp.call(to, key) && key !== except)
          __defProp(to, key, { get: () => from[key], enumerable: !(desc = __getOwnPropDesc(from, key)) || desc.enumerable });
    }
    return to;
  };
  var __toCommonJS = (mod) => __copyProps(__defProp({}, "__esModule", { value: true }), mod);

  // input.js
  var input_exports = {};
  __export(input_exports, {
    argon2id: () => argon2id,
    blake2b: () => blake2b,
    blake2s: () => blake2s,
    blake3: () => blake3,
    cshake128: () => cshake128,
    cshake256: () => cshake256,
    eskdf: () => eskdf,
    hkdf: () => hkdf,
    hmac: () => hmac,
    k12: () => k12,
    keccak_224: () => keccak_224,
    keccak_256: () => keccak_256,
    keccak_384: () => keccak_384,
    keccak_512: () => keccak_512,
    kmac128: () => kmac128,
    kmac256: () => kmac256,
    m14: () => m14,
    pbkdf2: () => pbkdf2,
    pbkdf2Async: () => pbkdf2Async,
    ripemd160: () => ripemd160,
    scrypt: () => scrypt,
    scryptAsync: () => scryptAsync,
    sha1: () => sha1,
    sha256: () => sha256,
    sha3_224: () => sha3_224,
    sha3_256: () => sha3_256,
    sha3_384: () => sha3_384,
    sha3_512: () => sha3_512,
    sha512: () => sha512,
    turboshake128: () => turboshake128,
    turboshake256: () => turboshake256,
    utils: () => utils
  });

  // ../src/crypto.ts
  var crypto = typeof globalThis === "object" && "crypto" in globalThis ? globalThis.crypto : void 0;

  // ../esm/_assert.js
  function number(n) {
    if (!Number.isSafeInteger(n) || n < 0)
      throw new Error(`positive integer expected, not ${n}`);
  }
  function isBytes(a) {
    return a instanceof Uint8Array || a != null && typeof a === "object" && a.constructor.name === "Uint8Array";
  }
  function bytes(b, ...lengths) {
    if (!isBytes(b))
      throw new Error("Uint8Array expected");
    if (lengths.length > 0 && !lengths.includes(b.length))
      throw new Error(`Uint8Array expected of length ${lengths}, not of length=${b.length}`);
  }
  function hash(h) {
    if (typeof h !== "function" || typeof h.create !== "function")
      throw new Error("Hash should be wrapped by utils.wrapConstructor");
    number(h.outputLen);
    number(h.blockLen);
  }
  function exists(instance, checkFinished = true) {
    if (instance.destroyed)
      throw new Error("Hash instance has been destroyed");
    if (checkFinished && instance.finished)
      throw new Error("Hash#digest() has already been called");
  }
  function output(out, instance) {
    bytes(out);
    const min = instance.outputLen;
    if (out.length < min) {
      throw new Error(`digestInto() expects output buffer of length at least ${min}`);
    }
  }

  // ../esm/utils.js
  var u8 = (arr) => new Uint8Array(arr.buffer, arr.byteOffset, arr.byteLength);
  var u32 = (arr) => new Uint32Array(arr.buffer, arr.byteOffset, Math.floor(arr.byteLength / 4));
  var createView = (arr) => new DataView(arr.buffer, arr.byteOffset, arr.byteLength);
  var rotr = (word, shift) => word << 32 - shift | word >>> shift;
  var rotl = (word, shift) => word << shift | word >>> 32 - shift >>> 0;
  var isLE = new Uint8Array(new Uint32Array([287454020]).buffer)[0] === 68;
  var byteSwap = (word) => word << 24 & 4278190080 | word << 8 & 16711680 | word >>> 8 & 65280 | word >>> 24 & 255;
  var byteSwapIfBE = isLE ? (n) => n : (n) => byteSwap(n);
  function byteSwap32(arr) {
    for (let i = 0; i < arr.length; i++) {
      arr[i] = byteSwap(arr[i]);
    }
  }
  var hexes = /* @__PURE__ */ Array.from({ length: 256 }, (_, i) => i.toString(16).padStart(2, "0"));
  function bytesToHex(bytes2) {
    bytes(bytes2);
    let hex = "";
    for (let i = 0; i < bytes2.length; i++) {
      hex += hexes[bytes2[i]];
    }
    return hex;
  }
  var asciis = { _0: 48, _9: 57, _A: 65, _F: 70, _a: 97, _f: 102 };
  function asciiToBase16(char) {
    if (char >= asciis._0 && char <= asciis._9)
      return char - asciis._0;
    if (char >= asciis._A && char <= asciis._F)
      return char - (asciis._A - 10);
    if (char >= asciis._a && char <= asciis._f)
      return char - (asciis._a - 10);
    return;
  }
  function hexToBytes(hex) {
    if (typeof hex !== "string")
      throw new Error("hex string expected, got " + typeof hex);
    const hl = hex.length;
    const al = hl / 2;
    if (hl % 2)
      throw new Error("padded hex string expected, got unpadded hex of length " + hl);
    const array = new Uint8Array(al);
    for (let ai = 0, hi = 0; ai < al; ai++, hi += 2) {
      const n1 = asciiToBase16(hex.charCodeAt(hi));
      const n2 = asciiToBase16(hex.charCodeAt(hi + 1));
      if (n1 === void 0 || n2 === void 0) {
        const char = hex[hi] + hex[hi + 1];
        throw new Error('hex string expected, got non-hex character "' + char + '" at index ' + hi);
      }
      array[ai] = n1 * 16 + n2;
    }
    return array;
  }
  var nextTick = async () => {
  };
  async function asyncLoop(iters, tick, cb) {
    let ts = Date.now();
    for (let i = 0; i < iters; i++) {
      cb(i);
      const diff = Date.now() - ts;
      if (diff >= 0 && diff < tick)
        continue;
      await nextTick();
      ts += diff;
    }
  }
  function utf8ToBytes(str) {
    if (typeof str !== "string")
      throw new Error(`utf8ToBytes expected string, got ${typeof str}`);
    return new Uint8Array(new TextEncoder().encode(str));
  }
  function toBytes(data) {
    if (typeof data === "string")
      data = utf8ToBytes(data);
    bytes(data);
    return data;
  }
  function concatBytes(...arrays) {
    let sum = 0;
    for (let i = 0; i < arrays.length; i++) {
      const a = arrays[i];
      bytes(a);
      sum += a.length;
    }
    const res = new Uint8Array(sum);
    for (let i = 0, pad = 0; i < arrays.length; i++) {
      const a = arrays[i];
      res.set(a, pad);
      pad += a.length;
    }
    return res;
  }
  var Hash = class {
    // Safe version that clones internal state
    clone() {
      return this._cloneInto();
    }
  };
  var toStr = {}.toString;
  function checkOpts(defaults, opts) {
    if (opts !== void 0 && toStr.call(opts) !== "[object Object]")
      throw new Error("Options should be object or undefined");
    const merged = Object.assign(defaults, opts);
    return merged;
  }
  function wrapConstructor(hashCons) {
    const hashC = (msg) => hashCons().update(toBytes(msg)).digest();
    const tmp = hashCons();
    hashC.outputLen = tmp.outputLen;
    hashC.blockLen = tmp.blockLen;
    hashC.create = () => hashCons();
    return hashC;
  }
  function wrapConstructorWithOpts(hashCons) {
    const hashC = (msg, opts) => hashCons(opts).update(toBytes(msg)).digest();
    const tmp = hashCons({});
    hashC.outputLen = tmp.outputLen;
    hashC.blockLen = tmp.blockLen;
    hashC.create = (opts) => hashCons(opts);
    return hashC;
  }
  function wrapXOFConstructorWithOpts(hashCons) {
    const hashC = (msg, opts) => hashCons(opts).update(toBytes(msg)).digest();
    const tmp = hashCons({});
    hashC.outputLen = tmp.outputLen;
    hashC.blockLen = tmp.blockLen;
    hashC.create = (opts) => hashCons(opts);
    return hashC;
  }
  function randomBytes(bytesLength = 32) {
    if (crypto && typeof crypto.getRandomValues === "function") {
      return crypto.getRandomValues(new Uint8Array(bytesLength));
    }
    throw new Error("crypto.getRandomValues must be defined");
  }

  // ../esm/_blake.js
  var SIGMA = /* @__PURE__ */ new Uint8Array([
    0,
    1,
    2,
    3,
    4,
    5,
    6,
    7,
    8,
    9,
    10,
    11,
    12,
    13,
    14,
    15,
    14,
    10,
    4,
    8,
    9,
    15,
    13,
    6,
    1,
    12,
    0,
    2,
    11,
    7,
    5,
    3,
    11,
    8,
    12,
    0,
    5,
    2,
    15,
    13,
    10,
    14,
    3,
    6,
    7,
    1,
    9,
    4,
    7,
    9,
    3,
    1,
    13,
    12,
    11,
    14,
    2,
    6,
    5,
    10,
    4,
    0,
    15,
    8,
    9,
    0,
    5,
    7,
    2,
    4,
    10,
    15,
    14,
    1,
    11,
    12,
    6,
    8,
    3,
    13,
    2,
    12,
    6,
    10,
    0,
    11,
    8,
    3,
    4,
    13,
    7,
    5,
    15,
    14,
    1,
    9,
    12,
    5,
    1,
    15,
    14,
    13,
    4,
    10,
    0,
    7,
    6,
    3,
    9,
    2,
    8,
    11,
    13,
    11,
    7,
    14,
    12,
    1,
    3,
    9,
    5,
    0,
    15,
    4,
    8,
    6,
    2,
    10,
    6,
    15,
    14,
    9,
    11,
    3,
    0,
    8,
    12,
    2,
    13,
    7,
    1,
    4,
    10,
    5,
    10,
    2,
    8,
    4,
    7,
    6,
    1,
    5,
    15,
    11,
    9,
    14,
    3,
    12,
    13,
    0,
    0,
    1,
    2,
    3,
    4,
    5,
    6,
    7,
    8,
    9,
    10,
    11,
    12,
    13,
    14,
    15,
    14,
    10,
    4,
    8,
    9,
    15,
    13,
    6,
    1,
    12,
    0,
    2,
    11,
    7,
    5,
    3
  ]);
  var BLAKE = class extends Hash {
    constructor(blockLen, outputLen, opts = {}, keyLen, saltLen, persLen) {
      super();
      this.blockLen = blockLen;
      this.outputLen = outputLen;
      this.length = 0;
      this.pos = 0;
      this.finished = false;
      this.destroyed = false;
      number(blockLen);
      number(outputLen);
      number(keyLen);
      if (outputLen < 0 || outputLen > keyLen)
        throw new Error("outputLen bigger than keyLen");
      if (opts.key !== void 0 && (opts.key.length < 1 || opts.key.length > keyLen))
        throw new Error(`key must be up 1..${keyLen} byte long or undefined`);
      if (opts.salt !== void 0 && opts.salt.length !== saltLen)
        throw new Error(`salt must be ${saltLen} byte long or undefined`);
      if (opts.personalization !== void 0 && opts.personalization.length !== persLen)
        throw new Error(`personalization must be ${persLen} byte long or undefined`);
      this.buffer32 = u32(this.buffer = new Uint8Array(blockLen));
    }
    update(data) {
      exists(this);
      const { blockLen, buffer, buffer32 } = this;
      data = toBytes(data);
      const len = data.length;
      const offset = data.byteOffset;
      const buf = data.buffer;
      for (let pos = 0; pos < len; ) {
        if (this.pos === blockLen) {
          if (!isLE)
            byteSwap32(buffer32);
          this.compress(buffer32, 0, false);
          if (!isLE)
            byteSwap32(buffer32);
          this.pos = 0;
        }
        const take = Math.min(blockLen - this.pos, len - pos);
        const dataOffset = offset + pos;
        if (take === blockLen && !(dataOffset % 4) && pos + take < len) {
          const data32 = new Uint32Array(buf, dataOffset, Math.floor((len - pos) / 4));
          if (!isLE)
            byteSwap32(data32);
          for (let pos32 = 0; pos + blockLen < len; pos32 += buffer32.length, pos += blockLen) {
            this.length += blockLen;
            this.compress(data32, pos32, false);
          }
          if (!isLE)
            byteSwap32(data32);
          continue;
        }
        buffer.set(data.subarray(pos, pos + take), this.pos);
        this.pos += take;
        this.length += take;
        pos += take;
      }
      return this;
    }
    digestInto(out) {
      exists(this);
      output(out, this);
      const { pos, buffer32 } = this;
      this.finished = true;
      this.buffer.subarray(pos).fill(0);
      if (!isLE)
        byteSwap32(buffer32);
      this.compress(buffer32, 0, true);
      if (!isLE)
        byteSwap32(buffer32);
      const out32 = u32(out);
      this.get().forEach((v, i) => out32[i] = byteSwapIfBE(v));
    }
    digest() {
      const { buffer, outputLen } = this;
      this.digestInto(buffer);
      const res = buffer.slice(0, outputLen);
      this.destroy();
      return res;
    }
    _cloneInto(to) {
      const { buffer, length, finished, destroyed, outputLen, pos } = this;
      to || (to = new this.constructor({ dkLen: outputLen }));
      to.set(...this.get());
      to.length = length;
      to.finished = finished;
      to.destroyed = destroyed;
      to.outputLen = outputLen;
      to.buffer.set(buffer);
      to.pos = pos;
      return to;
    }
  };

  // ../esm/_u64.js
  var U32_MASK64 = /* @__PURE__ */ BigInt(2 ** 32 - 1);
  var _32n = /* @__PURE__ */ BigInt(32);
  function fromBig(n, le = false) {
    if (le)
      return { h: Number(n & U32_MASK64), l: Number(n >> _32n & U32_MASK64) };
    return { h: Number(n >> _32n & U32_MASK64) | 0, l: Number(n & U32_MASK64) | 0 };
  }
  function split(lst, le = false) {
    let Ah = new Uint32Array(lst.length);
    let Al = new Uint32Array(lst.length);
    for (let i = 0; i < lst.length; i++) {
      const { h, l } = fromBig(lst[i], le);
      [Ah[i], Al[i]] = [h, l];
    }
    return [Ah, Al];
  }
  var toBig = (h, l) => BigInt(h >>> 0) << _32n | BigInt(l >>> 0);
  var shrSH = (h, _l, s) => h >>> s;
  var shrSL = (h, l, s) => h << 32 - s | l >>> s;
  var rotrSH = (h, l, s) => h >>> s | l << 32 - s;
  var rotrSL = (h, l, s) => h << 32 - s | l >>> s;
  var rotrBH = (h, l, s) => h << 64 - s | l >>> s - 32;
  var rotrBL = (h, l, s) => h >>> s - 32 | l << 64 - s;
  var rotr32H = (_h, l) => l;
  var rotr32L = (h, _l) => h;
  var rotlSH = (h, l, s) => h << s | l >>> 32 - s;
  var rotlSL = (h, l, s) => l << s | h >>> 32 - s;
  var rotlBH = (h, l, s) => l << s - 32 | h >>> 64 - s;
  var rotlBL = (h, l, s) => h << s - 32 | l >>> 64 - s;
  function add(Ah, Al, Bh, Bl) {
    const l = (Al >>> 0) + (Bl >>> 0);
    return { h: Ah + Bh + (l / 2 ** 32 | 0) | 0, l: l | 0 };
  }
  var add3L = (Al, Bl, Cl) => (Al >>> 0) + (Bl >>> 0) + (Cl >>> 0);
  var add3H = (low, Ah, Bh, Ch) => Ah + Bh + Ch + (low / 2 ** 32 | 0) | 0;
  var add4L = (Al, Bl, Cl, Dl) => (Al >>> 0) + (Bl >>> 0) + (Cl >>> 0) + (Dl >>> 0);
  var add4H = (low, Ah, Bh, Ch, Dh) => Ah + Bh + Ch + Dh + (low / 2 ** 32 | 0) | 0;
  var add5L = (Al, Bl, Cl, Dl, El) => (Al >>> 0) + (Bl >>> 0) + (Cl >>> 0) + (Dl >>> 0) + (El >>> 0);
  var add5H = (low, Ah, Bh, Ch, Dh, Eh) => Ah + Bh + Ch + Dh + Eh + (low / 2 ** 32 | 0) | 0;
  var u64 = {
    fromBig,
    split,
    toBig,
    shrSH,
    shrSL,
    rotrSH,
    rotrSL,
    rotrBH,
    rotrBL,
    rotr32H,
    rotr32L,
    rotlSH,
    rotlSL,
    rotlBH,
    rotlBL,
    add,
    add3L,
    add3H,
    add4L,
    add4H,
    add5H,
    add5L
  };
  var u64_default = u64;

  // ../esm/blake2b.js
  var B2B_IV = /* @__PURE__ */ new Uint32Array([
    4089235720,
    1779033703,
    2227873595,
    3144134277,
    4271175723,
    1013904242,
    1595750129,
    2773480762,
    2917565137,
    1359893119,
    725511199,
    2600822924,
    4215389547,
    528734635,
    327033209,
    1541459225
  ]);
  var BBUF = /* @__PURE__ */ new Uint32Array(32);
  function G1b(a, b, c, d, msg, x) {
    const Xl = msg[x], Xh = msg[x + 1];
    let Al = BBUF[2 * a], Ah = BBUF[2 * a + 1];
    let Bl = BBUF[2 * b], Bh = BBUF[2 * b + 1];
    let Cl = BBUF[2 * c], Ch = BBUF[2 * c + 1];
    let Dl = BBUF[2 * d], Dh = BBUF[2 * d + 1];
    let ll = u64_default.add3L(Al, Bl, Xl);
    Ah = u64_default.add3H(ll, Ah, Bh, Xh);
    Al = ll | 0;
    ({ Dh, Dl } = { Dh: Dh ^ Ah, Dl: Dl ^ Al });
    ({ Dh, Dl } = { Dh: u64_default.rotr32H(Dh, Dl), Dl: u64_default.rotr32L(Dh, Dl) });
    ({ h: Ch, l: Cl } = u64_default.add(Ch, Cl, Dh, Dl));
    ({ Bh, Bl } = { Bh: Bh ^ Ch, Bl: Bl ^ Cl });
    ({ Bh, Bl } = { Bh: u64_default.rotrSH(Bh, Bl, 24), Bl: u64_default.rotrSL(Bh, Bl, 24) });
    BBUF[2 * a] = Al, BBUF[2 * a + 1] = Ah;
    BBUF[2 * b] = Bl, BBUF[2 * b + 1] = Bh;
    BBUF[2 * c] = Cl, BBUF[2 * c + 1] = Ch;
    BBUF[2 * d] = Dl, BBUF[2 * d + 1] = Dh;
  }
  function G2b(a, b, c, d, msg, x) {
    const Xl = msg[x], Xh = msg[x + 1];
    let Al = BBUF[2 * a], Ah = BBUF[2 * a + 1];
    let Bl = BBUF[2 * b], Bh = BBUF[2 * b + 1];
    let Cl = BBUF[2 * c], Ch = BBUF[2 * c + 1];
    let Dl = BBUF[2 * d], Dh = BBUF[2 * d + 1];
    let ll = u64_default.add3L(Al, Bl, Xl);
    Ah = u64_default.add3H(ll, Ah, Bh, Xh);
    Al = ll | 0;
    ({ Dh, Dl } = { Dh: Dh ^ Ah, Dl: Dl ^ Al });
    ({ Dh, Dl } = { Dh: u64_default.rotrSH(Dh, Dl, 16), Dl: u64_default.rotrSL(Dh, Dl, 16) });
    ({ h: Ch, l: Cl } = u64_default.add(Ch, Cl, Dh, Dl));
    ({ Bh, Bl } = { Bh: Bh ^ Ch, Bl: Bl ^ Cl });
    ({ Bh, Bl } = { Bh: u64_default.rotrBH(Bh, Bl, 63), Bl: u64_default.rotrBL(Bh, Bl, 63) });
    BBUF[2 * a] = Al, BBUF[2 * a + 1] = Ah;
    BBUF[2 * b] = Bl, BBUF[2 * b + 1] = Bh;
    BBUF[2 * c] = Cl, BBUF[2 * c + 1] = Ch;
    BBUF[2 * d] = Dl, BBUF[2 * d + 1] = Dh;
  }
  var BLAKE2b = class extends BLAKE {
    constructor(opts = {}) {
      super(128, opts.dkLen === void 0 ? 64 : opts.dkLen, opts, 64, 16, 16);
      this.v0l = B2B_IV[0] | 0;
      this.v0h = B2B_IV[1] | 0;
      this.v1l = B2B_IV[2] | 0;
      this.v1h = B2B_IV[3] | 0;
      this.v2l = B2B_IV[4] | 0;
      this.v2h = B2B_IV[5] | 0;
      this.v3l = B2B_IV[6] | 0;
      this.v3h = B2B_IV[7] | 0;
      this.v4l = B2B_IV[8] | 0;
      this.v4h = B2B_IV[9] | 0;
      this.v5l = B2B_IV[10] | 0;
      this.v5h = B2B_IV[11] | 0;
      this.v6l = B2B_IV[12] | 0;
      this.v6h = B2B_IV[13] | 0;
      this.v7l = B2B_IV[14] | 0;
      this.v7h = B2B_IV[15] | 0;
      const keyLength = opts.key ? opts.key.length : 0;
      this.v0l ^= this.outputLen | keyLength << 8 | 1 << 16 | 1 << 24;
      if (opts.salt) {
        const salt = u32(toBytes(opts.salt));
        this.v4l ^= byteSwapIfBE(salt[0]);
        this.v4h ^= byteSwapIfBE(salt[1]);
        this.v5l ^= byteSwapIfBE(salt[2]);
        this.v5h ^= byteSwapIfBE(salt[3]);
      }
      if (opts.personalization) {
        const pers = u32(toBytes(opts.personalization));
        this.v6l ^= byteSwapIfBE(pers[0]);
        this.v6h ^= byteSwapIfBE(pers[1]);
        this.v7l ^= byteSwapIfBE(pers[2]);
        this.v7h ^= byteSwapIfBE(pers[3]);
      }
      if (opts.key) {
        const tmp = new Uint8Array(this.blockLen);
        tmp.set(toBytes(opts.key));
        this.update(tmp);
      }
    }
    // prettier-ignore
    get() {
      let { v0l, v0h, v1l, v1h, v2l, v2h, v3l, v3h, v4l, v4h, v5l, v5h, v6l, v6h, v7l, v7h } = this;
      return [v0l, v0h, v1l, v1h, v2l, v2h, v3l, v3h, v4l, v4h, v5l, v5h, v6l, v6h, v7l, v7h];
    }
    // prettier-ignore
    set(v0l, v0h, v1l, v1h, v2l, v2h, v3l, v3h, v4l, v4h, v5l, v5h, v6l, v6h, v7l, v7h) {
      this.v0l = v0l | 0;
      this.v0h = v0h | 0;
      this.v1l = v1l | 0;
      this.v1h = v1h | 0;
      this.v2l = v2l | 0;
      this.v2h = v2h | 0;
      this.v3l = v3l | 0;
      this.v3h = v3h | 0;
      this.v4l = v4l | 0;
      this.v4h = v4h | 0;
      this.v5l = v5l | 0;
      this.v5h = v5h | 0;
      this.v6l = v6l | 0;
      this.v6h = v6h | 0;
      this.v7l = v7l | 0;
      this.v7h = v7h | 0;
    }
    compress(msg, offset, isLast) {
      this.get().forEach((v, i) => BBUF[i] = v);
      BBUF.set(B2B_IV, 16);
      let { h, l } = u64_default.fromBig(BigInt(this.length));
      BBUF[24] = B2B_IV[8] ^ l;
      BBUF[25] = B2B_IV[9] ^ h;
      if (isLast) {
        BBUF[28] = ~BBUF[28];
        BBUF[29] = ~BBUF[29];
      }
      let j = 0;
      const s = SIGMA;
      for (let i = 0; i < 12; i++) {
        G1b(0, 4, 8, 12, msg, offset + 2 * s[j++]);
        G2b(0, 4, 8, 12, msg, offset + 2 * s[j++]);
        G1b(1, 5, 9, 13, msg, offset + 2 * s[j++]);
        G2b(1, 5, 9, 13, msg, offset + 2 * s[j++]);
        G1b(2, 6, 10, 14, msg, offset + 2 * s[j++]);
        G2b(2, 6, 10, 14, msg, offset + 2 * s[j++]);
        G1b(3, 7, 11, 15, msg, offset + 2 * s[j++]);
        G2b(3, 7, 11, 15, msg, offset + 2 * s[j++]);
        G1b(0, 5, 10, 15, msg, offset + 2 * s[j++]);
        G2b(0, 5, 10, 15, msg, offset + 2 * s[j++]);
        G1b(1, 6, 11, 12, msg, offset + 2 * s[j++]);
        G2b(1, 6, 11, 12, msg, offset + 2 * s[j++]);
        G1b(2, 7, 8, 13, msg, offset + 2 * s[j++]);
        G2b(2, 7, 8, 13, msg, offset + 2 * s[j++]);
        G1b(3, 4, 9, 14, msg, offset + 2 * s[j++]);
        G2b(3, 4, 9, 14, msg, offset + 2 * s[j++]);
      }
      this.v0l ^= BBUF[0] ^ BBUF[16];
      this.v0h ^= BBUF[1] ^ BBUF[17];
      this.v1l ^= BBUF[2] ^ BBUF[18];
      this.v1h ^= BBUF[3] ^ BBUF[19];
      this.v2l ^= BBUF[4] ^ BBUF[20];
      this.v2h ^= BBUF[5] ^ BBUF[21];
      this.v3l ^= BBUF[6] ^ BBUF[22];
      this.v3h ^= BBUF[7] ^ BBUF[23];
      this.v4l ^= BBUF[8] ^ BBUF[24];
      this.v4h ^= BBUF[9] ^ BBUF[25];
      this.v5l ^= BBUF[10] ^ BBUF[26];
      this.v5h ^= BBUF[11] ^ BBUF[27];
      this.v6l ^= BBUF[12] ^ BBUF[28];
      this.v6h ^= BBUF[13] ^ BBUF[29];
      this.v7l ^= BBUF[14] ^ BBUF[30];
      this.v7h ^= BBUF[15] ^ BBUF[31];
      BBUF.fill(0);
    }
    destroy() {
      this.destroyed = true;
      this.buffer32.fill(0);
      this.set(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0);
    }
  };
  var blake2b = /* @__PURE__ */ wrapConstructorWithOpts((opts) => new BLAKE2b(opts));

  // ../esm/blake2s.js
  var B2S_IV = /* @__PURE__ */ new Uint32Array([
    1779033703,
    3144134277,
    1013904242,
    2773480762,
    1359893119,
    2600822924,
    528734635,
    1541459225
  ]);
  function G1s(a, b, c, d, x) {
    a = a + b + x | 0;
    d = rotr(d ^ a, 16);
    c = c + d | 0;
    b = rotr(b ^ c, 12);
    return { a, b, c, d };
  }
  function G2s(a, b, c, d, x) {
    a = a + b + x | 0;
    d = rotr(d ^ a, 8);
    c = c + d | 0;
    b = rotr(b ^ c, 7);
    return { a, b, c, d };
  }
  function compress(s, offset, msg, rounds, v0, v1, v2, v3, v4, v5, v6, v7, v8, v9, v10, v11, v12, v13, v14, v15) {
    let j = 0;
    for (let i = 0; i < rounds; i++) {
      ({ a: v0, b: v4, c: v8, d: v12 } = G1s(v0, v4, v8, v12, msg[offset + s[j++]]));
      ({ a: v0, b: v4, c: v8, d: v12 } = G2s(v0, v4, v8, v12, msg[offset + s[j++]]));
      ({ a: v1, b: v5, c: v9, d: v13 } = G1s(v1, v5, v9, v13, msg[offset + s[j++]]));
      ({ a: v1, b: v5, c: v9, d: v13 } = G2s(v1, v5, v9, v13, msg[offset + s[j++]]));
      ({ a: v2, b: v6, c: v10, d: v14 } = G1s(v2, v6, v10, v14, msg[offset + s[j++]]));
      ({ a: v2, b: v6, c: v10, d: v14 } = G2s(v2, v6, v10, v14, msg[offset + s[j++]]));
      ({ a: v3, b: v7, c: v11, d: v15 } = G1s(v3, v7, v11, v15, msg[offset + s[j++]]));
      ({ a: v3, b: v7, c: v11, d: v15 } = G2s(v3, v7, v11, v15, msg[offset + s[j++]]));
      ({ a: v0, b: v5, c: v10, d: v15 } = G1s(v0, v5, v10, v15, msg[offset + s[j++]]));
      ({ a: v0, b: v5, c: v10, d: v15 } = G2s(v0, v5, v10, v15, msg[offset + s[j++]]));
      ({ a: v1, b: v6, c: v11, d: v12 } = G1s(v1, v6, v11, v12, msg[offset + s[j++]]));
      ({ a: v1, b: v6, c: v11, d: v12 } = G2s(v1, v6, v11, v12, msg[offset + s[j++]]));
      ({ a: v2, b: v7, c: v8, d: v13 } = G1s(v2, v7, v8, v13, msg[offset + s[j++]]));
      ({ a: v2, b: v7, c: v8, d: v13 } = G2s(v2, v7, v8, v13, msg[offset + s[j++]]));
      ({ a: v3, b: v4, c: v9, d: v14 } = G1s(v3, v4, v9, v14, msg[offset + s[j++]]));
      ({ a: v3, b: v4, c: v9, d: v14 } = G2s(v3, v4, v9, v14, msg[offset + s[j++]]));
    }
    return { v0, v1, v2, v3, v4, v5, v6, v7, v8, v9, v10, v11, v12, v13, v14, v15 };
  }
  var BLAKE2s = class extends BLAKE {
    constructor(opts = {}) {
      super(64, opts.dkLen === void 0 ? 32 : opts.dkLen, opts, 32, 8, 8);
      this.v0 = B2S_IV[0] | 0;
      this.v1 = B2S_IV[1] | 0;
      this.v2 = B2S_IV[2] | 0;
      this.v3 = B2S_IV[3] | 0;
      this.v4 = B2S_IV[4] | 0;
      this.v5 = B2S_IV[5] | 0;
      this.v6 = B2S_IV[6] | 0;
      this.v7 = B2S_IV[7] | 0;
      const keyLength = opts.key ? opts.key.length : 0;
      this.v0 ^= this.outputLen | keyLength << 8 | 1 << 16 | 1 << 24;
      if (opts.salt) {
        const salt = u32(toBytes(opts.salt));
        this.v4 ^= byteSwapIfBE(salt[0]);
        this.v5 ^= byteSwapIfBE(salt[1]);
      }
      if (opts.personalization) {
        const pers = u32(toBytes(opts.personalization));
        this.v6 ^= byteSwapIfBE(pers[0]);
        this.v7 ^= byteSwapIfBE(pers[1]);
      }
      if (opts.key) {
        const tmp = new Uint8Array(this.blockLen);
        tmp.set(toBytes(opts.key));
        this.update(tmp);
      }
    }
    get() {
      const { v0, v1, v2, v3, v4, v5, v6, v7 } = this;
      return [v0, v1, v2, v3, v4, v5, v6, v7];
    }
    // prettier-ignore
    set(v0, v1, v2, v3, v4, v5, v6, v7) {
      this.v0 = v0 | 0;
      this.v1 = v1 | 0;
      this.v2 = v2 | 0;
      this.v3 = v3 | 0;
      this.v4 = v4 | 0;
      this.v5 = v5 | 0;
      this.v6 = v6 | 0;
      this.v7 = v7 | 0;
    }
    compress(msg, offset, isLast) {
      const { h, l } = fromBig(BigInt(this.length));
      const { v0, v1, v2, v3, v4, v5, v6, v7, v8, v9, v10, v11, v12, v13, v14, v15 } = compress(SIGMA, offset, msg, 10, this.v0, this.v1, this.v2, this.v3, this.v4, this.v5, this.v6, this.v7, B2S_IV[0], B2S_IV[1], B2S_IV[2], B2S_IV[3], l ^ B2S_IV[4], h ^ B2S_IV[5], isLast ? ~B2S_IV[6] : B2S_IV[6], B2S_IV[7]);
      this.v0 ^= v0 ^ v8;
      this.v1 ^= v1 ^ v9;
      this.v2 ^= v2 ^ v10;
      this.v3 ^= v3 ^ v11;
      this.v4 ^= v4 ^ v12;
      this.v5 ^= v5 ^ v13;
      this.v6 ^= v6 ^ v14;
      this.v7 ^= v7 ^ v15;
    }
    destroy() {
      this.destroyed = true;
      this.buffer32.fill(0);
      this.set(0, 0, 0, 0, 0, 0, 0, 0);
    }
  };
  var blake2s = /* @__PURE__ */ wrapConstructorWithOpts((opts) => new BLAKE2s(opts));

  // ../esm/blake3.js
  var SIGMA2 = /* @__PURE__ */ (() => {
    const Id2 = Array.from({ length: 16 }, (_, i) => i);
    const permute = (arr) => [2, 6, 3, 10, 7, 0, 4, 13, 1, 11, 12, 5, 9, 14, 15, 8].map((i) => arr[i]);
    const res = [];
    for (let i = 0, v = Id2; i < 7; i++, v = permute(v))
      res.push(...v);
    return Uint8Array.from(res);
  })();
  var BLAKE3 = class _BLAKE3 extends BLAKE {
    constructor(opts = {}, flags = 0) {
      super(64, opts.dkLen === void 0 ? 32 : opts.dkLen, {}, Number.MAX_SAFE_INTEGER, 0, 0);
      this.flags = 0 | 0;
      this.chunkPos = 0;
      this.chunksDone = 0;
      this.stack = [];
      this.posOut = 0;
      this.bufferOut32 = new Uint32Array(16);
      this.chunkOut = 0;
      this.enableXOF = true;
      this.outputLen = opts.dkLen === void 0 ? 32 : opts.dkLen;
      number(this.outputLen);
      if (opts.key !== void 0 && opts.context !== void 0)
        throw new Error("Blake3: only key or context can be specified at same time");
      else if (opts.key !== void 0) {
        const key = toBytes(opts.key).slice();
        if (key.length !== 32)
          throw new Error("Blake3: key should be 32 byte");
        this.IV = u32(key);
        if (!isLE)
          byteSwap32(this.IV);
        this.flags = flags | 16;
      } else if (opts.context !== void 0) {
        const context_key = new _BLAKE3(
          { dkLen: 32 },
          32
          /* B3_Flags.DERIVE_KEY_CONTEXT */
        ).update(opts.context).digest();
        this.IV = u32(context_key);
        if (!isLE)
          byteSwap32(this.IV);
        this.flags = flags | 64;
      } else {
        this.IV = B2S_IV.slice();
        this.flags = flags;
      }
      this.state = this.IV.slice();
      this.bufferOut = u8(this.bufferOut32);
    }
    // Unused
    get() {
      return [];
    }
    set() {
    }
    b2Compress(counter, flags, buf, bufPos = 0) {
      const { state: s, pos } = this;
      const { h, l } = fromBig(BigInt(counter), true);
      const { v0, v1, v2, v3, v4, v5, v6, v7, v8, v9, v10, v11, v12, v13, v14, v15 } = compress(SIGMA2, bufPos, buf, 7, s[0], s[1], s[2], s[3], s[4], s[5], s[6], s[7], B2S_IV[0], B2S_IV[1], B2S_IV[2], B2S_IV[3], h, l, pos, flags);
      s[0] = v0 ^ v8;
      s[1] = v1 ^ v9;
      s[2] = v2 ^ v10;
      s[3] = v3 ^ v11;
      s[4] = v4 ^ v12;
      s[5] = v5 ^ v13;
      s[6] = v6 ^ v14;
      s[7] = v7 ^ v15;
    }
    compress(buf, bufPos = 0, isLast = false) {
      let flags = this.flags;
      if (!this.chunkPos)
        flags |= 1;
      if (this.chunkPos === 15 || isLast)
        flags |= 2;
      if (!isLast)
        this.pos = this.blockLen;
      this.b2Compress(this.chunksDone, flags, buf, bufPos);
      this.chunkPos += 1;
      if (this.chunkPos === 16 || isLast) {
        let chunk = this.state;
        this.state = this.IV.slice();
        for (let last, chunks = this.chunksDone + 1; isLast || !(chunks & 1); chunks >>= 1) {
          if (!(last = this.stack.pop()))
            break;
          this.buffer32.set(last, 0);
          this.buffer32.set(chunk, 8);
          this.pos = this.blockLen;
          this.b2Compress(0, this.flags | 4, this.buffer32, 0);
          chunk = this.state;
          this.state = this.IV.slice();
        }
        this.chunksDone++;
        this.chunkPos = 0;
        this.stack.push(chunk);
      }
      this.pos = 0;
    }
    _cloneInto(to) {
      to = super._cloneInto(to);
      const { IV, flags, state, chunkPos, posOut, chunkOut, stack, chunksDone } = this;
      to.state.set(state.slice());
      to.stack = stack.map((i) => Uint32Array.from(i));
      to.IV.set(IV);
      to.flags = flags;
      to.chunkPos = chunkPos;
      to.chunksDone = chunksDone;
      to.posOut = posOut;
      to.chunkOut = chunkOut;
      to.enableXOF = this.enableXOF;
      to.bufferOut32.set(this.bufferOut32);
      return to;
    }
    destroy() {
      this.destroyed = true;
      this.state.fill(0);
      this.buffer32.fill(0);
      this.IV.fill(0);
      this.bufferOut32.fill(0);
      for (let i of this.stack)
        i.fill(0);
    }
    // Same as b2Compress, but doesn't modify state and returns 16 u32 array (instead of 8)
    b2CompressOut() {
      const { state: s, pos, flags, buffer32, bufferOut32: out32 } = this;
      const { h, l } = fromBig(BigInt(this.chunkOut++));
      if (!isLE)
        byteSwap32(buffer32);
      const { v0, v1, v2, v3, v4, v5, v6, v7, v8, v9, v10, v11, v12, v13, v14, v15 } = compress(SIGMA2, 0, buffer32, 7, s[0], s[1], s[2], s[3], s[4], s[5], s[6], s[7], B2S_IV[0], B2S_IV[1], B2S_IV[2], B2S_IV[3], l, h, pos, flags);
      out32[0] = v0 ^ v8;
      out32[1] = v1 ^ v9;
      out32[2] = v2 ^ v10;
      out32[3] = v3 ^ v11;
      out32[4] = v4 ^ v12;
      out32[5] = v5 ^ v13;
      out32[6] = v6 ^ v14;
      out32[7] = v7 ^ v15;
      out32[8] = s[0] ^ v8;
      out32[9] = s[1] ^ v9;
      out32[10] = s[2] ^ v10;
      out32[11] = s[3] ^ v11;
      out32[12] = s[4] ^ v12;
      out32[13] = s[5] ^ v13;
      out32[14] = s[6] ^ v14;
      out32[15] = s[7] ^ v15;
      if (!isLE) {
        byteSwap32(buffer32);
        byteSwap32(out32);
      }
      this.posOut = 0;
    }
    finish() {
      if (this.finished)
        return;
      this.finished = true;
      this.buffer.fill(0, this.pos);
      let flags = this.flags | 8;
      if (this.stack.length) {
        flags |= 4;
        if (!isLE)
          byteSwap32(this.buffer32);
        this.compress(this.buffer32, 0, true);
        if (!isLE)
          byteSwap32(this.buffer32);
        this.chunksDone = 0;
        this.pos = this.blockLen;
      } else {
        flags |= (!this.chunkPos ? 1 : 0) | 2;
      }
      this.flags = flags;
      this.b2CompressOut();
    }
    writeInto(out) {
      exists(this, false);
      bytes(out);
      this.finish();
      const { blockLen, bufferOut } = this;
      for (let pos = 0, len = out.length; pos < len; ) {
        if (this.posOut >= blockLen)
          this.b2CompressOut();
        const take = Math.min(blockLen - this.posOut, len - pos);
        out.set(bufferOut.subarray(this.posOut, this.posOut + take), pos);
        this.posOut += take;
        pos += take;
      }
      return out;
    }
    xofInto(out) {
      if (!this.enableXOF)
        throw new Error("XOF is not possible after digest call");
      return this.writeInto(out);
    }
    xof(bytes2) {
      number(bytes2);
      return this.xofInto(new Uint8Array(bytes2));
    }
    digestInto(out) {
      output(out, this);
      if (this.finished)
        throw new Error("digest() was already called");
      this.enableXOF = false;
      this.writeInto(out);
      this.destroy();
      return out;
    }
    digest() {
      return this.digestInto(new Uint8Array(this.outputLen));
    }
  };
  var blake3 = /* @__PURE__ */ wrapXOFConstructorWithOpts((opts) => new BLAKE3(opts));

  // ../esm/hmac.js
  var HMAC = class extends Hash {
    constructor(hash2, _key) {
      super();
      this.finished = false;
      this.destroyed = false;
      hash(hash2);
      const key = toBytes(_key);
      this.iHash = hash2.create();
      if (typeof this.iHash.update !== "function")
        throw new Error("Expected instance of class which extends utils.Hash");
      this.blockLen = this.iHash.blockLen;
      this.outputLen = this.iHash.outputLen;
      const blockLen = this.blockLen;
      const pad = new Uint8Array(blockLen);
      pad.set(key.length > blockLen ? hash2.create().update(key).digest() : key);
      for (let i = 0; i < pad.length; i++)
        pad[i] ^= 54;
      this.iHash.update(pad);
      this.oHash = hash2.create();
      for (let i = 0; i < pad.length; i++)
        pad[i] ^= 54 ^ 92;
      this.oHash.update(pad);
      pad.fill(0);
    }
    update(buf) {
      exists(this);
      this.iHash.update(buf);
      return this;
    }
    digestInto(out) {
      exists(this);
      bytes(out, this.outputLen);
      this.finished = true;
      this.iHash.digestInto(out);
      this.oHash.update(out);
      this.oHash.digestInto(out);
      this.destroy();
    }
    digest() {
      const out = new Uint8Array(this.oHash.outputLen);
      this.digestInto(out);
      return out;
    }
    _cloneInto(to) {
      to || (to = Object.create(Object.getPrototypeOf(this), {}));
      const { oHash, iHash, finished, destroyed, blockLen, outputLen } = this;
      to = to;
      to.finished = finished;
      to.destroyed = destroyed;
      to.blockLen = blockLen;
      to.outputLen = outputLen;
      to.oHash = oHash._cloneInto(to.oHash);
      to.iHash = iHash._cloneInto(to.iHash);
      return to;
    }
    destroy() {
      this.destroyed = true;
      this.oHash.destroy();
      this.iHash.destroy();
    }
  };
  var hmac = (hash2, key, message) => new HMAC(hash2, key).update(message).digest();
  hmac.create = (hash2, key) => new HMAC(hash2, key);

  // ../esm/hkdf.js
  function extract(hash2, ikm, salt) {
    hash(hash2);
    if (salt === void 0)
      salt = new Uint8Array(hash2.outputLen);
    return hmac(hash2, toBytes(salt), toBytes(ikm));
  }
  var HKDF_COUNTER = /* @__PURE__ */ new Uint8Array([0]);
  var EMPTY_BUFFER = /* @__PURE__ */ new Uint8Array();
  function expand(hash2, prk, info, length = 32) {
    hash(hash2);
    number(length);
    if (length > 255 * hash2.outputLen)
      throw new Error("Length should be <= 255*HashLen");
    const blocks = Math.ceil(length / hash2.outputLen);
    if (info === void 0)
      info = EMPTY_BUFFER;
    const okm = new Uint8Array(blocks * hash2.outputLen);
    const HMAC2 = hmac.create(hash2, prk);
    const HMACTmp = HMAC2._cloneInto();
    const T = new Uint8Array(HMAC2.outputLen);
    for (let counter = 0; counter < blocks; counter++) {
      HKDF_COUNTER[0] = counter + 1;
      HMACTmp.update(counter === 0 ? EMPTY_BUFFER : T).update(info).update(HKDF_COUNTER).digestInto(T);
      okm.set(T, hash2.outputLen * counter);
      HMAC2._cloneInto(HMACTmp);
    }
    HMAC2.destroy();
    HMACTmp.destroy();
    T.fill(0);
    HKDF_COUNTER.fill(0);
    return okm.slice(0, length);
  }
  var hkdf = (hash2, ikm, salt, info, length) => expand(hash2, extract(hash2, ikm, salt), info, length);

  // ../esm/pbkdf2.js
  function pbkdf2Init(hash2, _password, _salt, _opts) {
    hash(hash2);
    const opts = checkOpts({ dkLen: 32, asyncTick: 10 }, _opts);
    const { c, dkLen, asyncTick } = opts;
    number(c);
    number(dkLen);
    number(asyncTick);
    if (c < 1)
      throw new Error("PBKDF2: iterations (c) should be >= 1");
    const password = toBytes(_password);
    const salt = toBytes(_salt);
    const DK = new Uint8Array(dkLen);
    const PRF = hmac.create(hash2, password);
    const PRFSalt = PRF._cloneInto().update(salt);
    return { c, dkLen, asyncTick, DK, PRF, PRFSalt };
  }
  function pbkdf2Output(PRF, PRFSalt, DK, prfW, u) {
    PRF.destroy();
    PRFSalt.destroy();
    if (prfW)
      prfW.destroy();
    u.fill(0);
    return DK;
  }
  function pbkdf2(hash2, password, salt, opts) {
    const { c, dkLen, DK, PRF, PRFSalt } = pbkdf2Init(hash2, password, salt, opts);
    let prfW;
    const arr = new Uint8Array(4);
    const view = createView(arr);
    const u = new Uint8Array(PRF.outputLen);
    for (let ti = 1, pos = 0; pos < dkLen; ti++, pos += PRF.outputLen) {
      const Ti = DK.subarray(pos, pos + PRF.outputLen);
      view.setInt32(0, ti, false);
      (prfW = PRFSalt._cloneInto(prfW)).update(arr).digestInto(u);
      Ti.set(u.subarray(0, Ti.length));
      for (let ui = 1; ui < c; ui++) {
        PRF._cloneInto(prfW).update(u).digestInto(u);
        for (let i = 0; i < Ti.length; i++)
          Ti[i] ^= u[i];
      }
    }
    return pbkdf2Output(PRF, PRFSalt, DK, prfW, u);
  }
  async function pbkdf2Async(hash2, password, salt, opts) {
    const { c, dkLen, asyncTick, DK, PRF, PRFSalt } = pbkdf2Init(hash2, password, salt, opts);
    let prfW;
    const arr = new Uint8Array(4);
    const view = createView(arr);
    const u = new Uint8Array(PRF.outputLen);
    for (let ti = 1, pos = 0; pos < dkLen; ti++, pos += PRF.outputLen) {
      const Ti = DK.subarray(pos, pos + PRF.outputLen);
      view.setInt32(0, ti, false);
      (prfW = PRFSalt._cloneInto(prfW)).update(arr).digestInto(u);
      Ti.set(u.subarray(0, Ti.length));
      await asyncLoop(c - 1, asyncTick, () => {
        PRF._cloneInto(prfW).update(u).digestInto(u);
        for (let i = 0; i < Ti.length; i++)
          Ti[i] ^= u[i];
      });
    }
    return pbkdf2Output(PRF, PRFSalt, DK, prfW, u);
  }

  // ../esm/_md.js
  function setBigUint64(view, byteOffset, value, isLE2) {
    if (typeof view.setBigUint64 === "function")
      return view.setBigUint64(byteOffset, value, isLE2);
    const _32n2 = BigInt(32);
    const _u32_max = BigInt(4294967295);
    const wh = Number(value >> _32n2 & _u32_max);
    const wl = Number(value & _u32_max);
    const h = isLE2 ? 4 : 0;
    const l = isLE2 ? 0 : 4;
    view.setUint32(byteOffset + h, wh, isLE2);
    view.setUint32(byteOffset + l, wl, isLE2);
  }
  var Chi = (a, b, c) => a & b ^ ~a & c;
  var Maj = (a, b, c) => a & b ^ a & c ^ b & c;
  var HashMD = class extends Hash {
    constructor(blockLen, outputLen, padOffset, isLE2) {
      super();
      this.blockLen = blockLen;
      this.outputLen = outputLen;
      this.padOffset = padOffset;
      this.isLE = isLE2;
      this.finished = false;
      this.length = 0;
      this.pos = 0;
      this.destroyed = false;
      this.buffer = new Uint8Array(blockLen);
      this.view = createView(this.buffer);
    }
    update(data) {
      exists(this);
      const { view, buffer, blockLen } = this;
      data = toBytes(data);
      const len = data.length;
      for (let pos = 0; pos < len; ) {
        const take = Math.min(blockLen - this.pos, len - pos);
        if (take === blockLen) {
          const dataView = createView(data);
          for (; blockLen <= len - pos; pos += blockLen)
            this.process(dataView, pos);
          continue;
        }
        buffer.set(data.subarray(pos, pos + take), this.pos);
        this.pos += take;
        pos += take;
        if (this.pos === blockLen) {
          this.process(view, 0);
          this.pos = 0;
        }
      }
      this.length += data.length;
      this.roundClean();
      return this;
    }
    digestInto(out) {
      exists(this);
      output(out, this);
      this.finished = true;
      const { buffer, view, blockLen, isLE: isLE2 } = this;
      let { pos } = this;
      buffer[pos++] = 128;
      this.buffer.subarray(pos).fill(0);
      if (this.padOffset > blockLen - pos) {
        this.process(view, 0);
        pos = 0;
      }
      for (let i = pos; i < blockLen; i++)
        buffer[i] = 0;
      setBigUint64(view, blockLen - 8, BigInt(this.length * 8), isLE2);
      this.process(view, 0);
      const oview = createView(out);
      const len = this.outputLen;
      if (len % 4)
        throw new Error("_sha2: outputLen should be aligned to 32bit");
      const outLen = len / 4;
      const state = this.get();
      if (outLen > state.length)
        throw new Error("_sha2: outputLen bigger than state");
      for (let i = 0; i < outLen; i++)
        oview.setUint32(4 * i, state[i], isLE2);
    }
    digest() {
      const { buffer, outputLen } = this;
      this.digestInto(buffer);
      const res = buffer.slice(0, outputLen);
      this.destroy();
      return res;
    }
    _cloneInto(to) {
      to || (to = new this.constructor());
      to.set(...this.get());
      const { blockLen, buffer, length, finished, destroyed, pos } = this;
      to.length = length;
      to.pos = pos;
      to.finished = finished;
      to.destroyed = destroyed;
      if (length % blockLen)
        to.buffer.set(buffer);
      return to;
    }
  };

  // ../esm/ripemd160.js
  var Rho = /* @__PURE__ */ new Uint8Array([7, 4, 13, 1, 10, 6, 15, 3, 12, 0, 9, 5, 2, 14, 11, 8]);
  var Id = /* @__PURE__ */ new Uint8Array(new Array(16).fill(0).map((_, i) => i));
  var Pi = /* @__PURE__ */ Id.map((i) => (9 * i + 5) % 16);
  var idxL = [Id];
  var idxR = [Pi];
  for (let i = 0; i < 4; i++)
    for (let j of [idxL, idxR])
      j.push(j[i].map((k) => Rho[k]));
  var shifts = /* @__PURE__ */ [
    [11, 14, 15, 12, 5, 8, 7, 9, 11, 13, 14, 15, 6, 7, 9, 8],
    [12, 13, 11, 15, 6, 9, 9, 7, 12, 15, 11, 13, 7, 8, 7, 7],
    [13, 15, 14, 11, 7, 7, 6, 8, 13, 14, 13, 12, 5, 5, 6, 9],
    [14, 11, 12, 14, 8, 6, 5, 5, 15, 12, 15, 14, 9, 9, 8, 6],
    [15, 12, 13, 13, 9, 5, 8, 6, 14, 11, 12, 11, 8, 6, 5, 5]
  ].map((i) => new Uint8Array(i));
  var shiftsL = /* @__PURE__ */ idxL.map((idx, i) => idx.map((j) => shifts[i][j]));
  var shiftsR = /* @__PURE__ */ idxR.map((idx, i) => idx.map((j) => shifts[i][j]));
  var Kl = /* @__PURE__ */ new Uint32Array([
    0,
    1518500249,
    1859775393,
    2400959708,
    2840853838
  ]);
  var Kr = /* @__PURE__ */ new Uint32Array([
    1352829926,
    1548603684,
    1836072691,
    2053994217,
    0
  ]);
  function f(group, x, y, z) {
    if (group === 0)
      return x ^ y ^ z;
    else if (group === 1)
      return x & y | ~x & z;
    else if (group === 2)
      return (x | ~y) ^ z;
    else if (group === 3)
      return x & z | y & ~z;
    else
      return x ^ (y | ~z);
  }
  var R_BUF = /* @__PURE__ */ new Uint32Array(16);
  var RIPEMD160 = class extends HashMD {
    constructor() {
      super(64, 20, 8, true);
      this.h0 = 1732584193 | 0;
      this.h1 = 4023233417 | 0;
      this.h2 = 2562383102 | 0;
      this.h3 = 271733878 | 0;
      this.h4 = 3285377520 | 0;
    }
    get() {
      const { h0, h1, h2, h3, h4 } = this;
      return [h0, h1, h2, h3, h4];
    }
    set(h0, h1, h2, h3, h4) {
      this.h0 = h0 | 0;
      this.h1 = h1 | 0;
      this.h2 = h2 | 0;
      this.h3 = h3 | 0;
      this.h4 = h4 | 0;
    }
    process(view, offset) {
      for (let i = 0; i < 16; i++, offset += 4)
        R_BUF[i] = view.getUint32(offset, true);
      let al = this.h0 | 0, ar = al, bl = this.h1 | 0, br = bl, cl = this.h2 | 0, cr = cl, dl = this.h3 | 0, dr = dl, el = this.h4 | 0, er = el;
      for (let group = 0; group < 5; group++) {
        const rGroup = 4 - group;
        const hbl = Kl[group], hbr = Kr[group];
        const rl = idxL[group], rr = idxR[group];
        const sl = shiftsL[group], sr = shiftsR[group];
        for (let i = 0; i < 16; i++) {
          const tl = rotl(al + f(group, bl, cl, dl) + R_BUF[rl[i]] + hbl, sl[i]) + el | 0;
          al = el, el = dl, dl = rotl(cl, 10) | 0, cl = bl, bl = tl;
        }
        for (let i = 0; i < 16; i++) {
          const tr = rotl(ar + f(rGroup, br, cr, dr) + R_BUF[rr[i]] + hbr, sr[i]) + er | 0;
          ar = er, er = dr, dr = rotl(cr, 10) | 0, cr = br, br = tr;
        }
      }
      this.set(this.h1 + cl + dr | 0, this.h2 + dl + er | 0, this.h3 + el + ar | 0, this.h4 + al + br | 0, this.h0 + bl + cr | 0);
    }
    roundClean() {
      R_BUF.fill(0);
    }
    destroy() {
      this.destroyed = true;
      this.buffer.fill(0);
      this.set(0, 0, 0, 0, 0);
    }
  };
  var ripemd160 = /* @__PURE__ */ wrapConstructor(() => new RIPEMD160());

  // ../esm/sha256.js
  var SHA256_K = /* @__PURE__ */ new Uint32Array([
    1116352408,
    1899447441,
    3049323471,
    3921009573,
    961987163,
    1508970993,
    2453635748,
    2870763221,
    3624381080,
    310598401,
    607225278,
    1426881987,
    1925078388,
    2162078206,
    2614888103,
    3248222580,
    3835390401,
    4022224774,
    264347078,
    604807628,
    770255983,
    1249150122,
    1555081692,
    1996064986,
    2554220882,
    2821834349,
    2952996808,
    3210313671,
    3336571891,
    3584528711,
    113926993,
    338241895,
    666307205,
    773529912,
    1294757372,
    1396182291,
    1695183700,
    1986661051,
    2177026350,
    2456956037,
    2730485921,
    2820302411,
    3259730800,
    3345764771,
    3516065817,
    3600352804,
    4094571909,
    275423344,
    430227734,
    506948616,
    659060556,
    883997877,
    958139571,
    1322822218,
    1537002063,
    1747873779,
    1955562222,
    2024104815,
    2227730452,
    2361852424,
    2428436474,
    2756734187,
    3204031479,
    3329325298
  ]);
  var SHA256_IV = /* @__PURE__ */ new Uint32Array([
    1779033703,
    3144134277,
    1013904242,
    2773480762,
    1359893119,
    2600822924,
    528734635,
    1541459225
  ]);
  var SHA256_W = /* @__PURE__ */ new Uint32Array(64);
  var SHA256 = class extends HashMD {
    constructor() {
      super(64, 32, 8, false);
      this.A = SHA256_IV[0] | 0;
      this.B = SHA256_IV[1] | 0;
      this.C = SHA256_IV[2] | 0;
      this.D = SHA256_IV[3] | 0;
      this.E = SHA256_IV[4] | 0;
      this.F = SHA256_IV[5] | 0;
      this.G = SHA256_IV[6] | 0;
      this.H = SHA256_IV[7] | 0;
    }
    get() {
      const { A, B, C, D, E, F, G: G2, H } = this;
      return [A, B, C, D, E, F, G2, H];
    }
    // prettier-ignore
    set(A, B, C, D, E, F, G2, H) {
      this.A = A | 0;
      this.B = B | 0;
      this.C = C | 0;
      this.D = D | 0;
      this.E = E | 0;
      this.F = F | 0;
      this.G = G2 | 0;
      this.H = H | 0;
    }
    process(view, offset) {
      for (let i = 0; i < 16; i++, offset += 4)
        SHA256_W[i] = view.getUint32(offset, false);
      for (let i = 16; i < 64; i++) {
        const W15 = SHA256_W[i - 15];
        const W2 = SHA256_W[i - 2];
        const s0 = rotr(W15, 7) ^ rotr(W15, 18) ^ W15 >>> 3;
        const s1 = rotr(W2, 17) ^ rotr(W2, 19) ^ W2 >>> 10;
        SHA256_W[i] = s1 + SHA256_W[i - 7] + s0 + SHA256_W[i - 16] | 0;
      }
      let { A, B, C, D, E, F, G: G2, H } = this;
      for (let i = 0; i < 64; i++) {
        const sigma1 = rotr(E, 6) ^ rotr(E, 11) ^ rotr(E, 25);
        const T1 = H + sigma1 + Chi(E, F, G2) + SHA256_K[i] + SHA256_W[i] | 0;
        const sigma0 = rotr(A, 2) ^ rotr(A, 13) ^ rotr(A, 22);
        const T2 = sigma0 + Maj(A, B, C) | 0;
        H = G2;
        G2 = F;
        F = E;
        E = D + T1 | 0;
        D = C;
        C = B;
        B = A;
        A = T1 + T2 | 0;
      }
      A = A + this.A | 0;
      B = B + this.B | 0;
      C = C + this.C | 0;
      D = D + this.D | 0;
      E = E + this.E | 0;
      F = F + this.F | 0;
      G2 = G2 + this.G | 0;
      H = H + this.H | 0;
      this.set(A, B, C, D, E, F, G2, H);
    }
    roundClean() {
      SHA256_W.fill(0);
    }
    destroy() {
      this.set(0, 0, 0, 0, 0, 0, 0, 0);
      this.buffer.fill(0);
    }
  };
  var sha256 = /* @__PURE__ */ wrapConstructor(() => new SHA256());

  // ../esm/scrypt.js
  function XorAndSalsa(prev, pi, input, ii, out, oi) {
    let y00 = prev[pi++] ^ input[ii++], y01 = prev[pi++] ^ input[ii++];
    let y02 = prev[pi++] ^ input[ii++], y03 = prev[pi++] ^ input[ii++];
    let y04 = prev[pi++] ^ input[ii++], y05 = prev[pi++] ^ input[ii++];
    let y06 = prev[pi++] ^ input[ii++], y07 = prev[pi++] ^ input[ii++];
    let y08 = prev[pi++] ^ input[ii++], y09 = prev[pi++] ^ input[ii++];
    let y10 = prev[pi++] ^ input[ii++], y11 = prev[pi++] ^ input[ii++];
    let y12 = prev[pi++] ^ input[ii++], y13 = prev[pi++] ^ input[ii++];
    let y14 = prev[pi++] ^ input[ii++], y15 = prev[pi++] ^ input[ii++];
    let x00 = y00, x01 = y01, x02 = y02, x03 = y03, x04 = y04, x05 = y05, x06 = y06, x07 = y07, x08 = y08, x09 = y09, x10 = y10, x11 = y11, x12 = y12, x13 = y13, x14 = y14, x15 = y15;
    for (let i = 0; i < 8; i += 2) {
      x04 ^= rotl(x00 + x12 | 0, 7);
      x08 ^= rotl(x04 + x00 | 0, 9);
      x12 ^= rotl(x08 + x04 | 0, 13);
      x00 ^= rotl(x12 + x08 | 0, 18);
      x09 ^= rotl(x05 + x01 | 0, 7);
      x13 ^= rotl(x09 + x05 | 0, 9);
      x01 ^= rotl(x13 + x09 | 0, 13);
      x05 ^= rotl(x01 + x13 | 0, 18);
      x14 ^= rotl(x10 + x06 | 0, 7);
      x02 ^= rotl(x14 + x10 | 0, 9);
      x06 ^= rotl(x02 + x14 | 0, 13);
      x10 ^= rotl(x06 + x02 | 0, 18);
      x03 ^= rotl(x15 + x11 | 0, 7);
      x07 ^= rotl(x03 + x15 | 0, 9);
      x11 ^= rotl(x07 + x03 | 0, 13);
      x15 ^= rotl(x11 + x07 | 0, 18);
      x01 ^= rotl(x00 + x03 | 0, 7);
      x02 ^= rotl(x01 + x00 | 0, 9);
      x03 ^= rotl(x02 + x01 | 0, 13);
      x00 ^= rotl(x03 + x02 | 0, 18);
      x06 ^= rotl(x05 + x04 | 0, 7);
      x07 ^= rotl(x06 + x05 | 0, 9);
      x04 ^= rotl(x07 + x06 | 0, 13);
      x05 ^= rotl(x04 + x07 | 0, 18);
      x11 ^= rotl(x10 + x09 | 0, 7);
      x08 ^= rotl(x11 + x10 | 0, 9);
      x09 ^= rotl(x08 + x11 | 0, 13);
      x10 ^= rotl(x09 + x08 | 0, 18);
      x12 ^= rotl(x15 + x14 | 0, 7);
      x13 ^= rotl(x12 + x15 | 0, 9);
      x14 ^= rotl(x13 + x12 | 0, 13);
      x15 ^= rotl(x14 + x13 | 0, 18);
    }
    out[oi++] = y00 + x00 | 0;
    out[oi++] = y01 + x01 | 0;
    out[oi++] = y02 + x02 | 0;
    out[oi++] = y03 + x03 | 0;
    out[oi++] = y04 + x04 | 0;
    out[oi++] = y05 + x05 | 0;
    out[oi++] = y06 + x06 | 0;
    out[oi++] = y07 + x07 | 0;
    out[oi++] = y08 + x08 | 0;
    out[oi++] = y09 + x09 | 0;
    out[oi++] = y10 + x10 | 0;
    out[oi++] = y11 + x11 | 0;
    out[oi++] = y12 + x12 | 0;
    out[oi++] = y13 + x13 | 0;
    out[oi++] = y14 + x14 | 0;
    out[oi++] = y15 + x15 | 0;
  }
  function BlockMix(input, ii, out, oi, r) {
    let head = oi + 0;
    let tail = oi + 16 * r;
    for (let i = 0; i < 16; i++)
      out[tail + i] = input[ii + (2 * r - 1) * 16 + i];
    for (let i = 0; i < r; i++, head += 16, ii += 16) {
      XorAndSalsa(out, tail, input, ii, out, head);
      if (i > 0)
        tail += 16;
      XorAndSalsa(out, head, input, ii += 16, out, tail);
    }
  }
  function scryptInit(password, salt, _opts) {
    const opts = checkOpts({
      dkLen: 32,
      asyncTick: 10,
      maxmem: 1024 ** 3 + 1024
    }, _opts);
    const { N, r, p, dkLen, asyncTick, maxmem, onProgress } = opts;
    number(N);
    number(r);
    number(p);
    number(dkLen);
    number(asyncTick);
    number(maxmem);
    if (onProgress !== void 0 && typeof onProgress !== "function")
      throw new Error("progressCb should be function");
    const blockSize = 128 * r;
    const blockSize32 = blockSize / 4;
    if (N <= 1 || (N & N - 1) !== 0 || N >= 2 ** (blockSize / 8) || N > 2 ** 32) {
      throw new Error("Scrypt: N must be larger than 1, a power of 2, less than 2^(128 * r / 8) and less than 2^32");
    }
    if (p < 0 || p > (2 ** 32 - 1) * 32 / blockSize) {
      throw new Error("Scrypt: p must be a positive integer less than or equal to ((2^32 - 1) * 32) / (128 * r)");
    }
    if (dkLen < 0 || dkLen > (2 ** 32 - 1) * 32) {
      throw new Error("Scrypt: dkLen should be positive integer less than or equal to (2^32 - 1) * 32");
    }
    const memUsed = blockSize * (N + p);
    if (memUsed > maxmem) {
      throw new Error(`Scrypt: parameters too large, ${memUsed} (128 * r * (N + p)) > ${maxmem} (maxmem)`);
    }
    const B = pbkdf2(sha256, password, salt, { c: 1, dkLen: blockSize * p });
    const B32 = u32(B);
    const V = u32(new Uint8Array(blockSize * N));
    const tmp = u32(new Uint8Array(blockSize));
    let blockMixCb = () => {
    };
    if (onProgress) {
      const totalBlockMix = 2 * N * p;
      const callbackPer = Math.max(Math.floor(totalBlockMix / 1e4), 1);
      let blockMixCnt = 0;
      blockMixCb = () => {
        blockMixCnt++;
        if (onProgress && (!(blockMixCnt % callbackPer) || blockMixCnt === totalBlockMix))
          onProgress(blockMixCnt / totalBlockMix);
      };
    }
    return { N, r, p, dkLen, blockSize32, V, B32, B, tmp, blockMixCb, asyncTick };
  }
  function scryptOutput(password, dkLen, B, V, tmp) {
    const res = pbkdf2(sha256, password, B, { c: 1, dkLen });
    B.fill(0);
    V.fill(0);
    tmp.fill(0);
    return res;
  }
  function scrypt(password, salt, opts) {
    const { N, r, p, dkLen, blockSize32, V, B32, B, tmp, blockMixCb } = scryptInit(password, salt, opts);
    if (!isLE)
      byteSwap32(B32);
    for (let pi = 0; pi < p; pi++) {
      const Pi2 = blockSize32 * pi;
      for (let i = 0; i < blockSize32; i++)
        V[i] = B32[Pi2 + i];
      for (let i = 0, pos = 0; i < N - 1; i++) {
        BlockMix(V, pos, V, pos += blockSize32, r);
        blockMixCb();
      }
      BlockMix(V, (N - 1) * blockSize32, B32, Pi2, r);
      blockMixCb();
      for (let i = 0; i < N; i++) {
        const j = B32[Pi2 + blockSize32 - 16] % N;
        for (let k = 0; k < blockSize32; k++)
          tmp[k] = B32[Pi2 + k] ^ V[j * blockSize32 + k];
        BlockMix(tmp, 0, B32, Pi2, r);
        blockMixCb();
      }
    }
    if (!isLE)
      byteSwap32(B32);
    return scryptOutput(password, dkLen, B, V, tmp);
  }
  async function scryptAsync(password, salt, opts) {
    const { N, r, p, dkLen, blockSize32, V, B32, B, tmp, blockMixCb, asyncTick } = scryptInit(password, salt, opts);
    if (!isLE)
      byteSwap32(B32);
    for (let pi = 0; pi < p; pi++) {
      const Pi2 = blockSize32 * pi;
      for (let i = 0; i < blockSize32; i++)
        V[i] = B32[Pi2 + i];
      let pos = 0;
      await asyncLoop(N - 1, asyncTick, () => {
        BlockMix(V, pos, V, pos += blockSize32, r);
        blockMixCb();
      });
      BlockMix(V, (N - 1) * blockSize32, B32, Pi2, r);
      blockMixCb();
      await asyncLoop(N, asyncTick, () => {
        const j = B32[Pi2 + blockSize32 - 16] % N;
        for (let k = 0; k < blockSize32; k++)
          tmp[k] = B32[Pi2 + k] ^ V[j * blockSize32 + k];
        BlockMix(tmp, 0, B32, Pi2, r);
        blockMixCb();
      });
    }
    if (!isLE)
      byteSwap32(B32);
    return scryptOutput(password, dkLen, B, V, tmp);
  }

  // ../esm/sha512.js
  var [SHA512_Kh, SHA512_Kl] = /* @__PURE__ */ (() => u64_default.split([
    "0x428a2f98d728ae22",
    "0x7137449123ef65cd",
    "0xb5c0fbcfec4d3b2f",
    "0xe9b5dba58189dbbc",
    "0x3956c25bf348b538",
    "0x59f111f1b605d019",
    "0x923f82a4af194f9b",
    "0xab1c5ed5da6d8118",
    "0xd807aa98a3030242",
    "0x12835b0145706fbe",
    "0x243185be4ee4b28c",
    "0x550c7dc3d5ffb4e2",
    "0x72be5d74f27b896f",
    "0x80deb1fe3b1696b1",
    "0x9bdc06a725c71235",
    "0xc19bf174cf692694",
    "0xe49b69c19ef14ad2",
    "0xefbe4786384f25e3",
    "0x0fc19dc68b8cd5b5",
    "0x240ca1cc77ac9c65",
    "0x2de92c6f592b0275",
    "0x4a7484aa6ea6e483",
    "0x5cb0a9dcbd41fbd4",
    "0x76f988da831153b5",
    "0x983e5152ee66dfab",
    "0xa831c66d2db43210",
    "0xb00327c898fb213f",
    "0xbf597fc7beef0ee4",
    "0xc6e00bf33da88fc2",
    "0xd5a79147930aa725",
    "0x06ca6351e003826f",
    "0x142929670a0e6e70",
    "0x27b70a8546d22ffc",
    "0x2e1b21385c26c926",
    "0x4d2c6dfc5ac42aed",
    "0x53380d139d95b3df",
    "0x650a73548baf63de",
    "0x766a0abb3c77b2a8",
    "0x81c2c92e47edaee6",
    "0x92722c851482353b",
    "0xa2bfe8a14cf10364",
    "0xa81a664bbc423001",
    "0xc24b8b70d0f89791",
    "0xc76c51a30654be30",
    "0xd192e819d6ef5218",
    "0xd69906245565a910",
    "0xf40e35855771202a",
    "0x106aa07032bbd1b8",
    "0x19a4c116b8d2d0c8",
    "0x1e376c085141ab53",
    "0x2748774cdf8eeb99",
    "0x34b0bcb5e19b48a8",
    "0x391c0cb3c5c95a63",
    "0x4ed8aa4ae3418acb",
    "0x5b9cca4f7763e373",
    "0x682e6ff3d6b2b8a3",
    "0x748f82ee5defb2fc",
    "0x78a5636f43172f60",
    "0x84c87814a1f0ab72",
    "0x8cc702081a6439ec",
    "0x90befffa23631e28",
    "0xa4506cebde82bde9",
    "0xbef9a3f7b2c67915",
    "0xc67178f2e372532b",
    "0xca273eceea26619c",
    "0xd186b8c721c0c207",
    "0xeada7dd6cde0eb1e",
    "0xf57d4f7fee6ed178",
    "0x06f067aa72176fba",
    "0x0a637dc5a2c898a6",
    "0x113f9804bef90dae",
    "0x1b710b35131c471b",
    "0x28db77f523047d84",
    "0x32caab7b40c72493",
    "0x3c9ebe0a15c9bebc",
    "0x431d67c49c100d4c",
    "0x4cc5d4becb3e42b6",
    "0x597f299cfc657e2a",
    "0x5fcb6fab3ad6faec",
    "0x6c44198c4a475817"
  ].map((n) => BigInt(n))))();
  var SHA512_W_H = /* @__PURE__ */ new Uint32Array(80);
  var SHA512_W_L = /* @__PURE__ */ new Uint32Array(80);
  var SHA512 = class extends HashMD {
    constructor() {
      super(128, 64, 16, false);
      this.Ah = 1779033703 | 0;
      this.Al = 4089235720 | 0;
      this.Bh = 3144134277 | 0;
      this.Bl = 2227873595 | 0;
      this.Ch = 1013904242 | 0;
      this.Cl = 4271175723 | 0;
      this.Dh = 2773480762 | 0;
      this.Dl = 1595750129 | 0;
      this.Eh = 1359893119 | 0;
      this.El = 2917565137 | 0;
      this.Fh = 2600822924 | 0;
      this.Fl = 725511199 | 0;
      this.Gh = 528734635 | 0;
      this.Gl = 4215389547 | 0;
      this.Hh = 1541459225 | 0;
      this.Hl = 327033209 | 0;
    }
    // prettier-ignore
    get() {
      const { Ah, Al, Bh, Bl, Ch, Cl, Dh, Dl, Eh, El, Fh, Fl, Gh, Gl, Hh, Hl } = this;
      return [Ah, Al, Bh, Bl, Ch, Cl, Dh, Dl, Eh, El, Fh, Fl, Gh, Gl, Hh, Hl];
    }
    // prettier-ignore
    set(Ah, Al, Bh, Bl, Ch, Cl, Dh, Dl, Eh, El, Fh, Fl, Gh, Gl, Hh, Hl) {
      this.Ah = Ah | 0;
      this.Al = Al | 0;
      this.Bh = Bh | 0;
      this.Bl = Bl | 0;
      this.Ch = Ch | 0;
      this.Cl = Cl | 0;
      this.Dh = Dh | 0;
      this.Dl = Dl | 0;
      this.Eh = Eh | 0;
      this.El = El | 0;
      this.Fh = Fh | 0;
      this.Fl = Fl | 0;
      this.Gh = Gh | 0;
      this.Gl = Gl | 0;
      this.Hh = Hh | 0;
      this.Hl = Hl | 0;
    }
    process(view, offset) {
      for (let i = 0; i < 16; i++, offset += 4) {
        SHA512_W_H[i] = view.getUint32(offset);
        SHA512_W_L[i] = view.getUint32(offset += 4);
      }
      for (let i = 16; i < 80; i++) {
        const W15h = SHA512_W_H[i - 15] | 0;
        const W15l = SHA512_W_L[i - 15] | 0;
        const s0h = u64_default.rotrSH(W15h, W15l, 1) ^ u64_default.rotrSH(W15h, W15l, 8) ^ u64_default.shrSH(W15h, W15l, 7);
        const s0l = u64_default.rotrSL(W15h, W15l, 1) ^ u64_default.rotrSL(W15h, W15l, 8) ^ u64_default.shrSL(W15h, W15l, 7);
        const W2h = SHA512_W_H[i - 2] | 0;
        const W2l = SHA512_W_L[i - 2] | 0;
        const s1h = u64_default.rotrSH(W2h, W2l, 19) ^ u64_default.rotrBH(W2h, W2l, 61) ^ u64_default.shrSH(W2h, W2l, 6);
        const s1l = u64_default.rotrSL(W2h, W2l, 19) ^ u64_default.rotrBL(W2h, W2l, 61) ^ u64_default.shrSL(W2h, W2l, 6);
        const SUMl = u64_default.add4L(s0l, s1l, SHA512_W_L[i - 7], SHA512_W_L[i - 16]);
        const SUMh = u64_default.add4H(SUMl, s0h, s1h, SHA512_W_H[i - 7], SHA512_W_H[i - 16]);
        SHA512_W_H[i] = SUMh | 0;
        SHA512_W_L[i] = SUMl | 0;
      }
      let { Ah, Al, Bh, Bl, Ch, Cl, Dh, Dl, Eh, El, Fh, Fl, Gh, Gl, Hh, Hl } = this;
      for (let i = 0; i < 80; i++) {
        const sigma1h = u64_default.rotrSH(Eh, El, 14) ^ u64_default.rotrSH(Eh, El, 18) ^ u64_default.rotrBH(Eh, El, 41);
        const sigma1l = u64_default.rotrSL(Eh, El, 14) ^ u64_default.rotrSL(Eh, El, 18) ^ u64_default.rotrBL(Eh, El, 41);
        const CHIh = Eh & Fh ^ ~Eh & Gh;
        const CHIl = El & Fl ^ ~El & Gl;
        const T1ll = u64_default.add5L(Hl, sigma1l, CHIl, SHA512_Kl[i], SHA512_W_L[i]);
        const T1h = u64_default.add5H(T1ll, Hh, sigma1h, CHIh, SHA512_Kh[i], SHA512_W_H[i]);
        const T1l = T1ll | 0;
        const sigma0h = u64_default.rotrSH(Ah, Al, 28) ^ u64_default.rotrBH(Ah, Al, 34) ^ u64_default.rotrBH(Ah, Al, 39);
        const sigma0l = u64_default.rotrSL(Ah, Al, 28) ^ u64_default.rotrBL(Ah, Al, 34) ^ u64_default.rotrBL(Ah, Al, 39);
        const MAJh = Ah & Bh ^ Ah & Ch ^ Bh & Ch;
        const MAJl = Al & Bl ^ Al & Cl ^ Bl & Cl;
        Hh = Gh | 0;
        Hl = Gl | 0;
        Gh = Fh | 0;
        Gl = Fl | 0;
        Fh = Eh | 0;
        Fl = El | 0;
        ({ h: Eh, l: El } = u64_default.add(Dh | 0, Dl | 0, T1h | 0, T1l | 0));
        Dh = Ch | 0;
        Dl = Cl | 0;
        Ch = Bh | 0;
        Cl = Bl | 0;
        Bh = Ah | 0;
        Bl = Al | 0;
        const All = u64_default.add3L(T1l, sigma0l, MAJl);
        Ah = u64_default.add3H(All, T1h, sigma0h, MAJh);
        Al = All | 0;
      }
      ({ h: Ah, l: Al } = u64_default.add(this.Ah | 0, this.Al | 0, Ah | 0, Al | 0));
      ({ h: Bh, l: Bl } = u64_default.add(this.Bh | 0, this.Bl | 0, Bh | 0, Bl | 0));
      ({ h: Ch, l: Cl } = u64_default.add(this.Ch | 0, this.Cl | 0, Ch | 0, Cl | 0));
      ({ h: Dh, l: Dl } = u64_default.add(this.Dh | 0, this.Dl | 0, Dh | 0, Dl | 0));
      ({ h: Eh, l: El } = u64_default.add(this.Eh | 0, this.El | 0, Eh | 0, El | 0));
      ({ h: Fh, l: Fl } = u64_default.add(this.Fh | 0, this.Fl | 0, Fh | 0, Fl | 0));
      ({ h: Gh, l: Gl } = u64_default.add(this.Gh | 0, this.Gl | 0, Gh | 0, Gl | 0));
      ({ h: Hh, l: Hl } = u64_default.add(this.Hh | 0, this.Hl | 0, Hh | 0, Hl | 0));
      this.set(Ah, Al, Bh, Bl, Ch, Cl, Dh, Dl, Eh, El, Fh, Fl, Gh, Gl, Hh, Hl);
    }
    roundClean() {
      SHA512_W_H.fill(0);
      SHA512_W_L.fill(0);
    }
    destroy() {
      this.buffer.fill(0);
      this.set(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0);
    }
  };
  var sha512 = /* @__PURE__ */ wrapConstructor(() => new SHA512());

  // ../esm/sha3.js
  var SHA3_PI = [];
  var SHA3_ROTL = [];
  var _SHA3_IOTA = [];
  var _0n = /* @__PURE__ */ BigInt(0);
  var _1n = /* @__PURE__ */ BigInt(1);
  var _2n = /* @__PURE__ */ BigInt(2);
  var _7n = /* @__PURE__ */ BigInt(7);
  var _256n = /* @__PURE__ */ BigInt(256);
  var _0x71n = /* @__PURE__ */ BigInt(113);
  for (let round = 0, R = _1n, x = 1, y = 0; round < 24; round++) {
    [x, y] = [y, (2 * x + 3 * y) % 5];
    SHA3_PI.push(2 * (5 * y + x));
    SHA3_ROTL.push((round + 1) * (round + 2) / 2 % 64);
    let t = _0n;
    for (let j = 0; j < 7; j++) {
      R = (R << _1n ^ (R >> _7n) * _0x71n) % _256n;
      if (R & _2n)
        t ^= _1n << (_1n << /* @__PURE__ */ BigInt(j)) - _1n;
    }
    _SHA3_IOTA.push(t);
  }
  var [SHA3_IOTA_H, SHA3_IOTA_L] = /* @__PURE__ */ split(_SHA3_IOTA, true);
  var rotlH = (h, l, s) => s > 32 ? rotlBH(h, l, s) : rotlSH(h, l, s);
  var rotlL = (h, l, s) => s > 32 ? rotlBL(h, l, s) : rotlSL(h, l, s);
  function keccakP(s, rounds = 24) {
    const B = new Uint32Array(5 * 2);
    for (let round = 24 - rounds; round < 24; round++) {
      for (let x = 0; x < 10; x++)
        B[x] = s[x] ^ s[x + 10] ^ s[x + 20] ^ s[x + 30] ^ s[x + 40];
      for (let x = 0; x < 10; x += 2) {
        const idx1 = (x + 8) % 10;
        const idx0 = (x + 2) % 10;
        const B0 = B[idx0];
        const B1 = B[idx0 + 1];
        const Th = rotlH(B0, B1, 1) ^ B[idx1];
        const Tl = rotlL(B0, B1, 1) ^ B[idx1 + 1];
        for (let y = 0; y < 50; y += 10) {
          s[x + y] ^= Th;
          s[x + y + 1] ^= Tl;
        }
      }
      let curH = s[2];
      let curL = s[3];
      for (let t = 0; t < 24; t++) {
        const shift = SHA3_ROTL[t];
        const Th = rotlH(curH, curL, shift);
        const Tl = rotlL(curH, curL, shift);
        const PI = SHA3_PI[t];
        curH = s[PI];
        curL = s[PI + 1];
        s[PI] = Th;
        s[PI + 1] = Tl;
      }
      for (let y = 0; y < 50; y += 10) {
        for (let x = 0; x < 10; x++)
          B[x] = s[y + x];
        for (let x = 0; x < 10; x++)
          s[y + x] ^= ~B[(x + 2) % 10] & B[(x + 4) % 10];
      }
      s[0] ^= SHA3_IOTA_H[round];
      s[1] ^= SHA3_IOTA_L[round];
    }
    B.fill(0);
  }
  var Keccak = class _Keccak extends Hash {
    // NOTE: we accept arguments in bytes instead of bits here.
    constructor(blockLen, suffix, outputLen, enableXOF = false, rounds = 24) {
      super();
      this.blockLen = blockLen;
      this.suffix = suffix;
      this.outputLen = outputLen;
      this.enableXOF = enableXOF;
      this.rounds = rounds;
      this.pos = 0;
      this.posOut = 0;
      this.finished = false;
      this.destroyed = false;
      number(outputLen);
      if (0 >= this.blockLen || this.blockLen >= 200)
        throw new Error("Sha3 supports only keccak-f1600 function");
      this.state = new Uint8Array(200);
      this.state32 = u32(this.state);
    }
    keccak() {
      if (!isLE)
        byteSwap32(this.state32);
      keccakP(this.state32, this.rounds);
      if (!isLE)
        byteSwap32(this.state32);
      this.posOut = 0;
      this.pos = 0;
    }
    update(data) {
      exists(this);
      const { blockLen, state } = this;
      data = toBytes(data);
      const len = data.length;
      for (let pos = 0; pos < len; ) {
        const take = Math.min(blockLen - this.pos, len - pos);
        for (let i = 0; i < take; i++)
          state[this.pos++] ^= data[pos++];
        if (this.pos === blockLen)
          this.keccak();
      }
      return this;
    }
    finish() {
      if (this.finished)
        return;
      this.finished = true;
      const { state, suffix, pos, blockLen } = this;
      state[pos] ^= suffix;
      if ((suffix & 128) !== 0 && pos === blockLen - 1)
        this.keccak();
      state[blockLen - 1] ^= 128;
      this.keccak();
    }
    writeInto(out) {
      exists(this, false);
      bytes(out);
      this.finish();
      const bufferOut = this.state;
      const { blockLen } = this;
      for (let pos = 0, len = out.length; pos < len; ) {
        if (this.posOut >= blockLen)
          this.keccak();
        const take = Math.min(blockLen - this.posOut, len - pos);
        out.set(bufferOut.subarray(this.posOut, this.posOut + take), pos);
        this.posOut += take;
        pos += take;
      }
      return out;
    }
    xofInto(out) {
      if (!this.enableXOF)
        throw new Error("XOF is not possible for this instance");
      return this.writeInto(out);
    }
    xof(bytes2) {
      number(bytes2);
      return this.xofInto(new Uint8Array(bytes2));
    }
    digestInto(out) {
      output(out, this);
      if (this.finished)
        throw new Error("digest() was already called");
      this.writeInto(out);
      this.destroy();
      return out;
    }
    digest() {
      return this.digestInto(new Uint8Array(this.outputLen));
    }
    destroy() {
      this.destroyed = true;
      this.state.fill(0);
    }
    _cloneInto(to) {
      const { blockLen, suffix, outputLen, rounds, enableXOF } = this;
      to || (to = new _Keccak(blockLen, suffix, outputLen, enableXOF, rounds));
      to.state32.set(this.state32);
      to.pos = this.pos;
      to.posOut = this.posOut;
      to.finished = this.finished;
      to.rounds = rounds;
      to.suffix = suffix;
      to.outputLen = outputLen;
      to.enableXOF = enableXOF;
      to.destroyed = this.destroyed;
      return to;
    }
  };
  var gen = (suffix, blockLen, outputLen) => wrapConstructor(() => new Keccak(blockLen, suffix, outputLen));
  var sha3_224 = /* @__PURE__ */ gen(6, 144, 224 / 8);
  var sha3_256 = /* @__PURE__ */ gen(6, 136, 256 / 8);
  var sha3_384 = /* @__PURE__ */ gen(6, 104, 384 / 8);
  var sha3_512 = /* @__PURE__ */ gen(6, 72, 512 / 8);
  var keccak_224 = /* @__PURE__ */ gen(1, 144, 224 / 8);
  var keccak_256 = /* @__PURE__ */ gen(1, 136, 256 / 8);
  var keccak_384 = /* @__PURE__ */ gen(1, 104, 384 / 8);
  var keccak_512 = /* @__PURE__ */ gen(1, 72, 512 / 8);
  var genShake = (suffix, blockLen, outputLen) => wrapXOFConstructorWithOpts((opts = {}) => new Keccak(blockLen, suffix, opts.dkLen === void 0 ? outputLen : opts.dkLen, true));
  var shake128 = /* @__PURE__ */ genShake(31, 168, 128 / 8);
  var shake256 = /* @__PURE__ */ genShake(31, 136, 256 / 8);

  // ../esm/sha3-addons.js
  function leftEncode(n) {
    const res = [n & 255];
    n >>= 8;
    for (; n > 0; n >>= 8)
      res.unshift(n & 255);
    res.unshift(res.length);
    return new Uint8Array(res);
  }
  function rightEncode(n) {
    const res = [n & 255];
    n >>= 8;
    for (; n > 0; n >>= 8)
      res.unshift(n & 255);
    res.push(res.length);
    return new Uint8Array(res);
  }
  function chooseLen(opts, outputLen) {
    return opts.dkLen === void 0 ? outputLen : opts.dkLen;
  }
  var toBytesOptional = (buf) => buf !== void 0 ? toBytes(buf) : new Uint8Array([]);
  var getPadding = (len, block2) => new Uint8Array((block2 - len % block2) % block2);
  function cshakePers(hash2, opts = {}) {
    if (!opts || !opts.personalization && !opts.NISTfn)
      return hash2;
    const blockLenBytes = leftEncode(hash2.blockLen);
    const fn = toBytesOptional(opts.NISTfn);
    const fnLen = leftEncode(8 * fn.length);
    const pers = toBytesOptional(opts.personalization);
    const persLen = leftEncode(8 * pers.length);
    if (!fn.length && !pers.length)
      return hash2;
    hash2.suffix = 4;
    hash2.update(blockLenBytes).update(fnLen).update(fn).update(persLen).update(pers);
    let totalLen = blockLenBytes.length + fnLen.length + fn.length + persLen.length + pers.length;
    hash2.update(getPadding(totalLen, hash2.blockLen));
    return hash2;
  }
  var gencShake = (suffix, blockLen, outputLen) => wrapXOFConstructorWithOpts((opts = {}) => cshakePers(new Keccak(blockLen, suffix, chooseLen(opts, outputLen), true), opts));
  var cshake128 = /* @__PURE__ */ (() => gencShake(31, 168, 128 / 8))();
  var cshake256 = /* @__PURE__ */ (() => gencShake(31, 136, 256 / 8))();
  var KMAC = class extends Keccak {
    constructor(blockLen, outputLen, enableXOF, key, opts = {}) {
      super(blockLen, 31, outputLen, enableXOF);
      cshakePers(this, { NISTfn: "KMAC", personalization: opts.personalization });
      key = toBytes(key);
      const blockLenBytes = leftEncode(this.blockLen);
      const keyLen = leftEncode(8 * key.length);
      this.update(blockLenBytes).update(keyLen).update(key);
      const totalLen = blockLenBytes.length + keyLen.length + key.length;
      this.update(getPadding(totalLen, this.blockLen));
    }
    finish() {
      if (!this.finished)
        this.update(rightEncode(this.enableXOF ? 0 : this.outputLen * 8));
      super.finish();
    }
    _cloneInto(to) {
      if (!to) {
        to = Object.create(Object.getPrototypeOf(this), {});
        to.state = this.state.slice();
        to.blockLen = this.blockLen;
        to.state32 = u32(to.state);
      }
      return super._cloneInto(to);
    }
    clone() {
      return this._cloneInto();
    }
  };
  function genKmac(blockLen, outputLen, xof = false) {
    const kmac = (key, message, opts) => kmac.create(key, opts).update(message).digest();
    kmac.create = (key, opts = {}) => new KMAC(blockLen, chooseLen(opts, outputLen), xof, key, opts);
    return kmac;
  }
  var kmac128 = /* @__PURE__ */ (() => genKmac(168, 128 / 8))();
  var kmac256 = /* @__PURE__ */ (() => genKmac(136, 256 / 8))();
  var genTurboshake = (blockLen, outputLen) => wrapXOFConstructorWithOpts((opts = {}) => {
    const D = opts.D === void 0 ? 31 : opts.D;
    if (!Number.isSafeInteger(D) || D < 1 || D > 127)
      throw new Error(`turboshake: wrong domain separation byte: ${D}, should be 0x01..0x7f`);
    return new Keccak(blockLen, D, opts.dkLen === void 0 ? outputLen : opts.dkLen, true, 12);
  });
  var turboshake128 = /* @__PURE__ */ genTurboshake(168, 256 / 8);
  var turboshake256 = /* @__PURE__ */ genTurboshake(136, 512 / 8);
  function rightEncodeK12(n) {
    const res = [];
    for (; n > 0; n >>= 8)
      res.unshift(n & 255);
    res.push(res.length);
    return new Uint8Array(res);
  }
  var EMPTY = new Uint8Array([]);
  var KangarooTwelve = class _KangarooTwelve extends Keccak {
    constructor(blockLen, leafLen, outputLen, rounds, opts) {
      super(blockLen, 7, outputLen, true, rounds);
      this.leafLen = leafLen;
      this.chunkLen = 8192;
      this.chunkPos = 0;
      this.chunksDone = 0;
      const { personalization } = opts;
      this.personalization = toBytesOptional(personalization);
    }
    update(data) {
      data = toBytes(data);
      const { chunkLen, blockLen, leafLen, rounds } = this;
      for (let pos = 0, len = data.length; pos < len; ) {
        if (this.chunkPos == chunkLen) {
          if (this.leafHash)
            super.update(this.leafHash.digest());
          else {
            this.suffix = 6;
            super.update(new Uint8Array([3, 0, 0, 0, 0, 0, 0, 0]));
          }
          this.leafHash = new Keccak(blockLen, 11, leafLen, false, rounds);
          this.chunksDone++;
          this.chunkPos = 0;
        }
        const take = Math.min(chunkLen - this.chunkPos, len - pos);
        const chunk = data.subarray(pos, pos + take);
        if (this.leafHash)
          this.leafHash.update(chunk);
        else
          super.update(chunk);
        this.chunkPos += take;
        pos += take;
      }
      return this;
    }
    finish() {
      if (this.finished)
        return;
      const { personalization } = this;
      this.update(personalization).update(rightEncodeK12(personalization.length));
      if (this.leafHash) {
        super.update(this.leafHash.digest());
        super.update(rightEncodeK12(this.chunksDone));
        super.update(new Uint8Array([255, 255]));
      }
      super.finish.call(this);
    }
    destroy() {
      super.destroy.call(this);
      if (this.leafHash)
        this.leafHash.destroy();
      this.personalization = EMPTY;
    }
    _cloneInto(to) {
      const { blockLen, leafLen, leafHash, outputLen, rounds } = this;
      to || (to = new _KangarooTwelve(blockLen, leafLen, outputLen, rounds, {}));
      super._cloneInto(to);
      if (leafHash)
        to.leafHash = leafHash._cloneInto(to.leafHash);
      to.personalization.set(this.personalization);
      to.leafLen = this.leafLen;
      to.chunkPos = this.chunkPos;
      to.chunksDone = this.chunksDone;
      return to;
    }
    clone() {
      return this._cloneInto();
    }
  };
  var k12 = /* @__PURE__ */ (() => wrapConstructorWithOpts((opts = {}) => new KangarooTwelve(168, 32, chooseLen(opts, 32), 12, opts)))();
  var m14 = /* @__PURE__ */ (() => wrapConstructorWithOpts((opts = {}) => new KangarooTwelve(136, 64, chooseLen(opts, 64), 14, opts)))();

  // ../esm/sha1.js
  var SHA1_IV = /* @__PURE__ */ new Uint32Array([
    1732584193,
    4023233417,
    2562383102,
    271733878,
    3285377520
  ]);
  var SHA1_W = /* @__PURE__ */ new Uint32Array(80);
  var SHA1 = class extends HashMD {
    constructor() {
      super(64, 20, 8, false);
      this.A = SHA1_IV[0] | 0;
      this.B = SHA1_IV[1] | 0;
      this.C = SHA1_IV[2] | 0;
      this.D = SHA1_IV[3] | 0;
      this.E = SHA1_IV[4] | 0;
    }
    get() {
      const { A, B, C, D, E } = this;
      return [A, B, C, D, E];
    }
    set(A, B, C, D, E) {
      this.A = A | 0;
      this.B = B | 0;
      this.C = C | 0;
      this.D = D | 0;
      this.E = E | 0;
    }
    process(view, offset) {
      for (let i = 0; i < 16; i++, offset += 4)
        SHA1_W[i] = view.getUint32(offset, false);
      for (let i = 16; i < 80; i++)
        SHA1_W[i] = rotl(SHA1_W[i - 3] ^ SHA1_W[i - 8] ^ SHA1_W[i - 14] ^ SHA1_W[i - 16], 1);
      let { A, B, C, D, E } = this;
      for (let i = 0; i < 80; i++) {
        let F, K;
        if (i < 20) {
          F = Chi(B, C, D);
          K = 1518500249;
        } else if (i < 40) {
          F = B ^ C ^ D;
          K = 1859775393;
        } else if (i < 60) {
          F = Maj(B, C, D);
          K = 2400959708;
        } else {
          F = B ^ C ^ D;
          K = 3395469782;
        }
        const T = rotl(A, 5) + F + E + K + SHA1_W[i] | 0;
        E = D;
        D = C;
        C = rotl(B, 30);
        B = A;
        A = T;
      }
      A = A + this.A | 0;
      B = B + this.B | 0;
      C = C + this.C | 0;
      D = D + this.D | 0;
      E = E + this.E | 0;
      this.set(A, B, C, D, E);
    }
    roundClean() {
      SHA1_W.fill(0);
    }
    destroy() {
      this.set(0, 0, 0, 0, 0);
      this.buffer.fill(0);
    }
  };
  var sha1 = /* @__PURE__ */ wrapConstructor(() => new SHA1());

  // ../esm/argon2.js
  var ARGON2_SYNC_POINTS = 4;
  var toBytesOptional2 = (buf) => buf !== void 0 ? toBytes(buf) : new Uint8Array([]);
  function mul(a, b) {
    const aL = a & 65535;
    const aH = a >>> 16;
    const bL = b & 65535;
    const bH = b >>> 16;
    const ll = Math.imul(aL, bL);
    const hl = Math.imul(aH, bL);
    const lh = Math.imul(aL, bH);
    const hh = Math.imul(aH, bH);
    const BUF = (ll >>> 16) + (hl & 65535) + lh | 0;
    const h = (hl >>> 16) + (BUF >>> 16) + hh | 0;
    return { h, l: BUF << 16 | ll & 65535 };
  }
  function relPos(areaSize, relativePos) {
    return areaSize - 1 - mul(areaSize, mul(relativePos, relativePos).h).h;
  }
  function mul2(a, b) {
    const { h, l } = mul(a, b);
    return { h: (h << 1 | l >>> 31) & 4294967295, l: l << 1 & 4294967295 };
  }
  function blamka(Ah, Al, Bh, Bl) {
    const { h: Ch, l: Cl } = mul2(Al, Bl);
    const Rll = add3L(Al, Bl, Cl);
    return { h: add3H(Rll, Ah, Bh, Ch), l: Rll | 0 };
  }
  var A2_BUF = new Uint32Array(256);
  function G(a, b, c, d) {
    let Al = A2_BUF[2 * a], Ah = A2_BUF[2 * a + 1];
    let Bl = A2_BUF[2 * b], Bh = A2_BUF[2 * b + 1];
    let Cl = A2_BUF[2 * c], Ch = A2_BUF[2 * c + 1];
    let Dl = A2_BUF[2 * d], Dh = A2_BUF[2 * d + 1];
    ({ h: Ah, l: Al } = blamka(Ah, Al, Bh, Bl));
    ({ Dh, Dl } = { Dh: Dh ^ Ah, Dl: Dl ^ Al });
    ({ Dh, Dl } = { Dh: rotr32H(Dh, Dl), Dl: rotr32L(Dh, Dl) });
    ({ h: Ch, l: Cl } = blamka(Ch, Cl, Dh, Dl));
    ({ Bh, Bl } = { Bh: Bh ^ Ch, Bl: Bl ^ Cl });
    ({ Bh, Bl } = { Bh: rotrSH(Bh, Bl, 24), Bl: rotrSL(Bh, Bl, 24) });
    ({ h: Ah, l: Al } = blamka(Ah, Al, Bh, Bl));
    ({ Dh, Dl } = { Dh: Dh ^ Ah, Dl: Dl ^ Al });
    ({ Dh, Dl } = { Dh: rotrSH(Dh, Dl, 16), Dl: rotrSL(Dh, Dl, 16) });
    ({ h: Ch, l: Cl } = blamka(Ch, Cl, Dh, Dl));
    ({ Bh, Bl } = { Bh: Bh ^ Ch, Bl: Bl ^ Cl });
    ({ Bh, Bl } = { Bh: rotrBH(Bh, Bl, 63), Bl: rotrBL(Bh, Bl, 63) });
    A2_BUF[2 * a] = Al, A2_BUF[2 * a + 1] = Ah;
    A2_BUF[2 * b] = Bl, A2_BUF[2 * b + 1] = Bh;
    A2_BUF[2 * c] = Cl, A2_BUF[2 * c + 1] = Ch;
    A2_BUF[2 * d] = Dl, A2_BUF[2 * d + 1] = Dh;
  }
  function P(v00, v01, v02, v03, v04, v05, v06, v07, v08, v09, v10, v11, v12, v13, v14, v15) {
    G(v00, v04, v08, v12);
    G(v01, v05, v09, v13);
    G(v02, v06, v10, v14);
    G(v03, v07, v11, v15);
    G(v00, v05, v10, v15);
    G(v01, v06, v11, v12);
    G(v02, v07, v08, v13);
    G(v03, v04, v09, v14);
  }
  function block(x, xPos, yPos, outPos, needXor) {
    for (let i = 0; i < 256; i++)
      A2_BUF[i] = x[xPos + i] ^ x[yPos + i];
    for (let i = 0; i < 128; i += 16) {
      P(i, i + 1, i + 2, i + 3, i + 4, i + 5, i + 6, i + 7, i + 8, i + 9, i + 10, i + 11, i + 12, i + 13, i + 14, i + 15);
    }
    for (let i = 0; i < 16; i += 2) {
      P(i, i + 1, i + 16, i + 17, i + 32, i + 33, i + 48, i + 49, i + 64, i + 65, i + 80, i + 81, i + 96, i + 97, i + 112, i + 113);
    }
    if (needXor)
      for (let i = 0; i < 256; i++)
        x[outPos + i] ^= A2_BUF[i] ^ x[xPos + i] ^ x[yPos + i];
    else
      for (let i = 0; i < 256; i++)
        x[outPos + i] = A2_BUF[i] ^ x[xPos + i] ^ x[yPos + i];
  }
  function Hp(A, dkLen) {
    const A8 = u8(A);
    const T = new Uint32Array(1);
    const T8 = u8(T);
    T[0] = dkLen;
    if (dkLen <= 64)
      return blake2b.create({ dkLen }).update(T8).update(A8).digest();
    const out = new Uint8Array(dkLen);
    let V = blake2b.create({}).update(T8).update(A8).digest();
    let pos = 0;
    out.set(V.subarray(0, 32));
    pos += 32;
    for (; dkLen - pos > 64; pos += 32)
      out.set((V = blake2b(V)).subarray(0, 32), pos);
    out.set(blake2b(V, { dkLen: dkLen - pos }), pos);
    return u32(out);
  }
  function indexAlpha(r, s, laneLen, segmentLen, index, randL, sameLane = false) {
    let area;
    if (0 == r) {
      if (0 == s)
        area = index - 1;
      else if (sameLane)
        area = s * segmentLen + index - 1;
      else
        area = s * segmentLen + (index == 0 ? -1 : 0);
    } else if (sameLane)
      area = laneLen - segmentLen + index - 1;
    else
      area = laneLen - segmentLen + (index == 0 ? -1 : 0);
    const startPos = r !== 0 && s !== ARGON2_SYNC_POINTS - 1 ? (s + 1) * segmentLen : 0;
    const rel = relPos(area, randL);
    return (startPos + rel) % laneLen;
  }
  function argon2Init(type, password, salt, opts) {
    password = toBytes(password);
    salt = toBytes(salt);
    let { p, dkLen, m, t, version, key, personalization, maxmem, onProgress } = {
      ...opts,
      version: opts.version || 19,
      dkLen: opts.dkLen || 32,
      maxmem: 2 ** 32
    };
    number(p);
    number(dkLen);
    number(m);
    number(t);
    number(version);
    if (dkLen < 4 || dkLen >= 2 ** 32)
      throw new Error("Argon2: dkLen should be at least 4 bytes");
    if (p < 1 || p >= 2 ** 32)
      throw new Error("Argon2: p (parallelism) should be at least 1");
    if (t < 1 || t >= 2 ** 32)
      throw new Error("Argon2: t (iterations) should be at least 1");
    if (m < 8 * p)
      throw new Error(`Argon2: memory should be at least 8*p bytes`);
    if (version !== 16 && version !== 19)
      throw new Error(`Argon2: unknown version=${version}`);
    password = toBytes(password);
    if (password.length < 0 || password.length >= 2 ** 32)
      throw new Error("Argon2: password should be less than 4 GB");
    salt = toBytes(salt);
    if (salt.length < 8)
      throw new Error("Argon2: salt should be at least 8 bytes");
    key = toBytesOptional2(key);
    personalization = toBytesOptional2(personalization);
    if (onProgress !== void 0 && typeof onProgress !== "function")
      throw new Error("progressCb should be function");
    const lanes = p;
    const mP = 4 * p * Math.floor(m / (ARGON2_SYNC_POINTS * p));
    const laneLen = Math.floor(mP / p);
    const segmentLen = Math.floor(laneLen / ARGON2_SYNC_POINTS);
    const h = blake2b.create({});
    const BUF = new Uint32Array(1);
    const BUF8 = u8(BUF);
    for (const i of [p, dkLen, m, t, version, type]) {
      if (i < 0 || i >= 2 ** 32)
        throw new Error(`Argon2: wrong parameter=${i}, expected uint32`);
      BUF[0] = i;
      h.update(BUF8);
    }
    for (let i of [password, salt, key, personalization]) {
      BUF[0] = i.length;
      h.update(BUF8).update(i);
    }
    const H0 = new Uint32Array(18);
    const H0_8 = u8(H0);
    h.digestInto(H0_8);
    const memUsed = mP * 256;
    if (memUsed < 0 || memUsed >= 2 ** 32 || memUsed > maxmem) {
      throw new Error(`Argon2: wrong params (memUsed=${memUsed} maxmem=${maxmem}), should be less than 2**32`);
    }
    const B = new Uint32Array(memUsed);
    for (let l = 0; l < p; l++) {
      const i = 256 * laneLen * l;
      H0[17] = l;
      H0[16] = 0;
      B.set(Hp(H0, 1024), i);
      H0[16] = 1;
      B.set(Hp(H0, 1024), i + 256);
    }
    let perBlock = () => {
    };
    if (onProgress) {
      const totalBlock = t * ARGON2_SYNC_POINTS * p * segmentLen;
      const callbackPer = Math.max(Math.floor(totalBlock / 1e4), 1);
      let blockCnt = 0;
      perBlock = () => {
        blockCnt++;
        if (onProgress && (!(blockCnt % callbackPer) || blockCnt === totalBlock))
          onProgress(blockCnt / totalBlock);
      };
    }
    return { type, mP, p, t, version, B, laneLen, lanes, segmentLen, dkLen, perBlock };
  }
  function argon2Output(B, p, laneLen, dkLen) {
    const B_final = new Uint32Array(256);
    for (let l = 0; l < p; l++)
      for (let j = 0; j < 256; j++)
        B_final[j] ^= B[256 * (laneLen * l + laneLen - 1) + j];
    return u8(Hp(B_final, dkLen));
  }
  function processBlock(B, address, l, r, s, index, laneLen, segmentLen, lanes, offset, prev, dataIndependent, needXor) {
    if (offset % laneLen)
      prev = offset - 1;
    let randL, randH;
    if (dataIndependent) {
      if (index % 128 === 0) {
        address[256 + 12]++;
        block(address, 256, 2 * 256, 0, false);
        block(address, 0, 2 * 256, 0, false);
      }
      randL = address[2 * (index % 128)];
      randH = address[2 * (index % 128) + 1];
    } else {
      const T = 256 * prev;
      randL = B[T];
      randH = B[T + 1];
    }
    const refLane = r === 0 && s === 0 ? l : randH % lanes;
    const refPos = indexAlpha(r, s, laneLen, segmentLen, index, randL, refLane == l);
    const refBlock = laneLen * refLane + refPos;
    block(B, 256 * prev, 256 * refBlock, offset * 256, needXor);
  }
  function argon2(type, password, salt, opts) {
    const { mP, p, t, version, B, laneLen, lanes, segmentLen, dkLen, perBlock } = argon2Init(type, password, salt, opts);
    const address = new Uint32Array(3 * 256);
    address[256 + 6] = mP;
    address[256 + 8] = t;
    address[256 + 10] = type;
    for (let r = 0; r < t; r++) {
      const needXor = r !== 0 && version === 19;
      address[256 + 0] = r;
      for (let s = 0; s < ARGON2_SYNC_POINTS; s++) {
        address[256 + 4] = s;
        const dataIndependent = type == 1 || type == 2 && r === 0 && s < 2;
        for (let l = 0; l < p; l++) {
          address[256 + 2] = l;
          address[256 + 12] = 0;
          let startPos = 0;
          if (r === 0 && s === 0) {
            startPos = 2;
            if (dataIndependent) {
              address[256 + 12]++;
              block(address, 256, 2 * 256, 0, false);
              block(address, 0, 2 * 256, 0, false);
            }
          }
          let offset = l * laneLen + s * segmentLen + startPos;
          let prev = offset % laneLen ? offset - 1 : offset + laneLen - 1;
          for (let index = startPos; index < segmentLen; index++, offset++, prev++) {
            perBlock();
            processBlock(B, address, l, r, s, index, laneLen, segmentLen, lanes, offset, prev, dataIndependent, needXor);
          }
        }
      }
    }
    return argon2Output(B, p, laneLen, dkLen);
  }
  var argon2id = (password, salt, opts) => argon2(2, password, salt, opts);

  // ../esm/eskdf.js
  var SCRYPT_FACTOR = 2 ** 19;
  var PBKDF2_FACTOR = 2 ** 17;
  function scrypt2(password, salt) {
    return scrypt(password, salt, { N: SCRYPT_FACTOR, r: 8, p: 1, dkLen: 32 });
  }
  function pbkdf22(password, salt) {
    return pbkdf2(sha256, password, salt, { c: PBKDF2_FACTOR, dkLen: 32 });
  }
  function xor32(a, b) {
    bytes(a, 32);
    bytes(b, 32);
    const arr = new Uint8Array(32);
    for (let i = 0; i < 32; i++) {
      arr[i] = a[i] ^ b[i];
    }
    return arr;
  }
  function strHasLength(str, min, max) {
    return typeof str === "string" && str.length >= min && str.length <= max;
  }
  function deriveMainSeed(username, password) {
    if (!strHasLength(username, 8, 255))
      throw new Error("invalid username");
    if (!strHasLength(password, 8, 255))
      throw new Error("invalid password");
    const scr = scrypt2(password + "", username + "");
    const pbk = pbkdf22(password + "", username + "");
    const res = xor32(scr, pbk);
    scr.fill(0);
    pbk.fill(0);
    return res;
  }
  function getSaltInfo(protocol, accountId = 0) {
    if (!(strHasLength(protocol, 3, 15) && /^[a-z0-9]{3,15}$/.test(protocol))) {
      throw new Error("invalid protocol");
    }
    const allowsStr = /^password\d{0,3}|ssh|tor|file$/.test(protocol);
    let salt;
    if (typeof accountId === "string") {
      if (!allowsStr)
        throw new Error("accountId must be a number");
      if (!strHasLength(accountId, 1, 255))
        throw new Error("accountId must be valid string");
      salt = toBytes(accountId);
    } else if (Number.isSafeInteger(accountId)) {
      if (accountId < 0 || accountId > 2 ** 32 - 1)
        throw new Error("invalid accountId");
      salt = new Uint8Array(4);
      createView(salt).setUint32(0, accountId, false);
    } else {
      throw new Error(`accountId must be a number${allowsStr ? " or string" : ""}`);
    }
    const info = toBytes(protocol);
    return { salt, info };
  }
  function countBytes(num) {
    if (typeof num !== "bigint" || num <= BigInt(128))
      throw new Error("invalid number");
    return Math.ceil(num.toString(2).length / 8);
  }
  function getKeyLength(options) {
    if (!options || typeof options !== "object")
      return 32;
    const hasLen = "keyLength" in options;
    const hasMod = "modulus" in options;
    if (hasLen && hasMod)
      throw new Error("cannot combine keyLength and modulus options");
    if (!hasLen && !hasMod)
      throw new Error("must have either keyLength or modulus option");
    const l = hasMod ? countBytes(options.modulus) + 8 : options.keyLength;
    if (!(typeof l === "number" && l >= 16 && l <= 8192))
      throw new Error("invalid keyLength");
    return l;
  }
  function modReduceKey(key, modulus) {
    const _1 = BigInt(1);
    const num = BigInt("0x" + bytesToHex(key));
    const res = num % (modulus - _1) + _1;
    if (res < _1)
      throw new Error("expected positive number");
    const len = key.length - 8;
    const hex = res.toString(16).padStart(len * 2, "0");
    const bytes2 = hexToBytes(hex);
    if (bytes2.length !== len)
      throw new Error("invalid length of result key");
    return bytes2;
  }
  async function eskdf(username, password) {
    let seed = deriveMainSeed(username, password);
    function deriveCK(protocol, accountId = 0, options) {
      bytes(seed, 32);
      const { salt, info } = getSaltInfo(protocol, accountId);
      const keyLength = getKeyLength(options);
      const key = hkdf(sha256, seed, salt, info, keyLength);
      return options && "modulus" in options ? modReduceKey(key, options.modulus) : key;
    }
    function expire() {
      if (seed)
        seed.fill(1);
      seed = void 0;
    }
    const fingerprint = Array.from(deriveCK("fingerprint", 0)).slice(0, 6).map((char) => char.toString(16).padStart(2, "0").toUpperCase()).join(":");
    return Object.freeze({ deriveChildKey: deriveCK, expire, fingerprint });
  }

  // input.js
  var utils = { bytesToHex, hexToBytes, concatBytes, utf8ToBytes, randomBytes };
  return __toCommonJS(input_exports);
})();
/*! noble-hashes - MIT License (c) 2022 Paul Miller (paulmillr.com) */
"use strict";
var nobleCurves = (() => {
  var __defProp = Object.defineProperty;
  var __getOwnPropDesc = Object.getOwnPropertyDescriptor;
  var __getOwnPropNames = Object.getOwnPropertyNames;
  var __hasOwnProp = Object.prototype.hasOwnProperty;
  var __export = (target, all) => {
    for (var name in all)
      __defProp(target, name, { get: all[name], enumerable: true });
  };
  var __copyProps = (to, from, except, desc) => {
    if (from && typeof from === "object" || typeof from === "function") {
      for (let key of __getOwnPropNames(from))
        if (!__hasOwnProp.call(to, key) && key !== except)
          __defProp(to, key, { get: () => from[key], enumerable: !(desc = __getOwnPropDesc(from, key)) || desc.enumerable });
    }
    return to;
  };
  var __toCommonJS = (mod2) => __copyProps(__defProp({}, "__esModule", { value: true }), mod2);

  // input.js
  var input_exports = {};
  __export(input_exports, {
    bls12_381: () => bls12_381,
    ed25519: () => ed25519,
    ed25519_edwardsToMontgomeryPriv: () => edwardsToMontgomeryPriv,
    ed25519_edwardsToMontgomeryPub: () => edwardsToMontgomeryPub,
    ed448: () => ed448,
    ed448_edwardsToMontgomeryPub: () => edwardsToMontgomeryPub2,
    p256: () => p256,
    p384: () => p384,
    p521: () => p521,
    secp256k1: () => secp256k1,
    secp256k1_schnorr: () => schnorr,
    utils: () => utils,
    x25519: () => x25519,
    x448: () => x448
  });

  // ../esm/abstract/utils.js
  var utils_exports = {};
  __export(utils_exports, {
    abytes: () => abytes,
    bitGet: () => bitGet,
    bitLen: () => bitLen,
    bitMask: () => bitMask,
    bitSet: () => bitSet,
    bytesToHex: () => bytesToHex,
    bytesToNumberBE: () => bytesToNumberBE,
    bytesToNumberLE: () => bytesToNumberLE,
    concatBytes: () => concatBytes,
    createHmacDrbg: () => createHmacDrbg,
    ensureBytes: () => ensureBytes,
    equalBytes: () => equalBytes,
    hexToBytes: () => hexToBytes,
    hexToNumber: () => hexToNumber,
    isBytes: () => isBytes,
    numberToBytesBE: () => numberToBytesBE,
    numberToBytesLE: () => numberToBytesLE,
    numberToHexUnpadded: () => numberToHexUnpadded,
    numberToVarBytesBE: () => numberToVarBytesBE,
    utf8ToBytes: () => utf8ToBytes,
    validateObject: () => validateObject
  });
  var _0n = BigInt(0);
  var _1n = BigInt(1);
  var _2n = BigInt(2);
  function isBytes(a) {
    return a instanceof Uint8Array || a != null && typeof a === "object" && a.constructor.name === "Uint8Array";
  }
  function abytes(item) {
    if (!isBytes(item))
      throw new Error("Uint8Array expected");
  }
  var hexes = /* @__PURE__ */ Array.from({ length: 256 }, (_, i) => i.toString(16).padStart(2, "0"));
  function bytesToHex(bytes2) {
    abytes(bytes2);
    let hex = "";
    for (let i = 0; i < bytes2.length; i++) {
      hex += hexes[bytes2[i]];
    }
    return hex;
  }
  function numberToHexUnpadded(num) {
    const hex = num.toString(16);
    return hex.length & 1 ? `0${hex}` : hex;
  }
  function hexToNumber(hex) {
    if (typeof hex !== "string")
      throw new Error("hex string expected, got " + typeof hex);
    return BigInt(hex === "" ? "0" : `0x${hex}`);
  }
  var asciis = { _0: 48, _9: 57, _A: 65, _F: 70, _a: 97, _f: 102 };
  function asciiToBase16(char) {
    if (char >= asciis._0 && char <= asciis._9)
      return char - asciis._0;
    if (char >= asciis._A && char <= asciis._F)
      return char - (asciis._A - 10);
    if (char >= asciis._a && char <= asciis._f)
      return char - (asciis._a - 10);
    return;
  }
  function hexToBytes(hex) {
    if (typeof hex !== "string")
      throw new Error("hex string expected, got " + typeof hex);
    const hl = hex.length;
    const al = hl / 2;
    if (hl % 2)
      throw new Error("padded hex string expected, got unpadded hex of length " + hl);
    const array = new Uint8Array(al);
    for (let ai = 0, hi = 0; ai < al; ai++, hi += 2) {
      const n1 = asciiToBase16(hex.charCodeAt(hi));
      const n2 = asciiToBase16(hex.charCodeAt(hi + 1));
      if (n1 === void 0 || n2 === void 0) {
        const char = hex[hi] + hex[hi + 1];
        throw new Error('hex string expected, got non-hex character "' + char + '" at index ' + hi);
      }
      array[ai] = n1 * 16 + n2;
    }
    return array;
  }
  function bytesToNumberBE(bytes2) {
    return hexToNumber(bytesToHex(bytes2));
  }
  function bytesToNumberLE(bytes2) {
    abytes(bytes2);
    return hexToNumber(bytesToHex(Uint8Array.from(bytes2).reverse()));
  }
  function numberToBytesBE(n, len) {
    return hexToBytes(n.toString(16).padStart(len * 2, "0"));
  }
  function numberToBytesLE(n, len) {
    return numberToBytesBE(n, len).reverse();
  }
  function numberToVarBytesBE(n) {
    return hexToBytes(numberToHexUnpadded(n));
  }
  function ensureBytes(title, hex, expectedLength) {
    let res;
    if (typeof hex === "string") {
      try {
        res = hexToBytes(hex);
      } catch (e) {
        throw new Error(`${title} must be valid hex string, got "${hex}". Cause: ${e}`);
      }
    } else if (isBytes(hex)) {
      res = Uint8Array.from(hex);
    } else {
      throw new Error(`${title} must be hex string or Uint8Array`);
    }
    const len = res.length;
    if (typeof expectedLength === "number" && len !== expectedLength)
      throw new Error(`${title} expected ${expectedLength} bytes, got ${len}`);
    return res;
  }
  function concatBytes(...arrays) {
    let sum = 0;
    for (let i = 0; i < arrays.length; i++) {
      const a = arrays[i];
      abytes(a);
      sum += a.length;
    }
    const res = new Uint8Array(sum);
    for (let i = 0, pad = 0; i < arrays.length; i++) {
      const a = arrays[i];
      res.set(a, pad);
      pad += a.length;
    }
    return res;
  }
  function equalBytes(a, b) {
    if (a.length !== b.length)
      return false;
    let diff = 0;
    for (let i = 0; i < a.length; i++)
      diff |= a[i] ^ b[i];
    return diff === 0;
  }
  function utf8ToBytes(str) {
    if (typeof str !== "string")
      throw new Error(`utf8ToBytes expected string, got ${typeof str}`);
    return new Uint8Array(new TextEncoder().encode(str));
  }
  function bitLen(n) {
    let len;
    for (len = 0; n > _0n; n >>= _1n, len += 1)
      ;
    return len;
  }
  function bitGet(n, pos) {
    return n >> BigInt(pos) & _1n;
  }
  function bitSet(n, pos, value) {
    return n | (value ? _1n : _0n) << BigInt(pos);
  }
  var bitMask = (n) => (_2n << BigInt(n - 1)) - _1n;
  var u8n = (data) => new Uint8Array(data);
  var u8fr = (arr) => Uint8Array.from(arr);
  function createHmacDrbg(hashLen, qByteLen, hmacFn) {
    if (typeof hashLen !== "number" || hashLen < 2)
      throw new Error("hashLen must be a number");
    if (typeof qByteLen !== "number" || qByteLen < 2)
      throw new Error("qByteLen must be a number");
    if (typeof hmacFn !== "function")
      throw new Error("hmacFn must be a function");
    let v = u8n(hashLen);
    let k = u8n(hashLen);
    let i = 0;
    const reset = () => {
      v.fill(1);
      k.fill(0);
      i = 0;
    };
    const h = (...b) => hmacFn(k, v, ...b);
    const reseed = (seed = u8n()) => {
      k = h(u8fr([0]), seed);
      v = h();
      if (seed.length === 0)
        return;
      k = h(u8fr([1]), seed);
      v = h();
    };
    const gen2 = () => {
      if (i++ >= 1e3)
        throw new Error("drbg: tried 1000 values");
      let len = 0;
      const out = [];
      while (len < qByteLen) {
        v = h();
        const sl = v.slice();
        out.push(sl);
        len += v.length;
      }
      return concatBytes(...out);
    };
    const genUntil = (seed, pred) => {
      reset();
      reseed(seed);
      let res = void 0;
      while (!(res = pred(gen2())))
        reseed();
      reset();
      return res;
    };
    return genUntil;
  }
  var validatorFns = {
    bigint: (val) => typeof val === "bigint",
    function: (val) => typeof val === "function",
    boolean: (val) => typeof val === "boolean",
    string: (val) => typeof val === "string",
    stringOrUint8Array: (val) => typeof val === "string" || isBytes(val),
    isSafeInteger: (val) => Number.isSafeInteger(val),
    array: (val) => Array.isArray(val),
    field: (val, object) => object.Fp.isValid(val),
    hash: (val) => typeof val === "function" && Number.isSafeInteger(val.outputLen)
  };
  function validateObject(object, validators, optValidators = {}) {
    const checkField = (fieldName, type, isOptional) => {
      const checkVal = validatorFns[type];
      if (typeof checkVal !== "function")
        throw new Error(`Invalid validator "${type}", expected function`);
      const val = object[fieldName];
      if (isOptional && val === void 0)
        return;
      if (!checkVal(val, object)) {
        throw new Error(`Invalid param ${String(fieldName)}=${val} (${typeof val}), expected ${type}`);
      }
    };
    for (const [fieldName, type] of Object.entries(validators))
      checkField(fieldName, type, false);
    for (const [fieldName, type] of Object.entries(optValidators))
      checkField(fieldName, type, true);
    return object;
  }

  // ../node_modules/@noble/hashes/esm/_assert.js
  function number(n) {
    if (!Number.isSafeInteger(n) || n < 0)
      throw new Error(`positive integer expected, not ${n}`);
  }
  function isBytes2(a) {
    return a instanceof Uint8Array || a != null && typeof a === "object" && a.constructor.name === "Uint8Array";
  }
  function bytes(b, ...lengths) {
    if (!isBytes2(b))
      throw new Error("Uint8Array expected");
    if (lengths.length > 0 && !lengths.includes(b.length))
      throw new Error(`Uint8Array expected of length ${lengths}, not of length=${b.length}`);
  }
  function hash(h) {
    if (typeof h !== "function" || typeof h.create !== "function")
      throw new Error("Hash should be wrapped by utils.wrapConstructor");
    number(h.outputLen);
    number(h.blockLen);
  }
  function exists(instance, checkFinished = true) {
    if (instance.destroyed)
      throw new Error("Hash instance has been destroyed");
    if (checkFinished && instance.finished)
      throw new Error("Hash#digest() has already been called");
  }
  function output(out, instance) {
    bytes(out);
    const min = instance.outputLen;
    if (out.length < min) {
      throw new Error(`digestInto() expects output buffer of length at least ${min}`);
    }
  }

  // ../node_modules/@noble/hashes/esm/crypto.js
  var crypto = typeof globalThis === "object" && "crypto" in globalThis ? globalThis.crypto : void 0;

  // ../node_modules/@noble/hashes/esm/utils.js
  var u32 = (arr) => new Uint32Array(arr.buffer, arr.byteOffset, Math.floor(arr.byteLength / 4));
  var createView = (arr) => new DataView(arr.buffer, arr.byteOffset, arr.byteLength);
  var rotr = (word, shift) => word << 32 - shift | word >>> shift;
  var isLE = new Uint8Array(new Uint32Array([287454020]).buffer)[0] === 68;
  var byteSwap = (word) => word << 24 & 4278190080 | word << 8 & 16711680 | word >>> 8 & 65280 | word >>> 24 & 255;
  function byteSwap32(arr) {
    for (let i = 0; i < arr.length; i++) {
      arr[i] = byteSwap(arr[i]);
    }
  }
  function utf8ToBytes2(str) {
    if (typeof str !== "string")
      throw new Error(`utf8ToBytes expected string, got ${typeof str}`);
    return new Uint8Array(new TextEncoder().encode(str));
  }
  function toBytes(data) {
    if (typeof data === "string")
      data = utf8ToBytes2(data);
    bytes(data);
    return data;
  }
  function concatBytes2(...arrays) {
    let sum = 0;
    for (let i = 0; i < arrays.length; i++) {
      const a = arrays[i];
      bytes(a);
      sum += a.length;
    }
    const res = new Uint8Array(sum);
    for (let i = 0, pad = 0; i < arrays.length; i++) {
      const a = arrays[i];
      res.set(a, pad);
      pad += a.length;
    }
    return res;
  }
  var Hash = class {
    // Safe version that clones internal state
    clone() {
      return this._cloneInto();
    }
  };
  var toStr = {}.toString;
  function wrapConstructor(hashCons) {
    const hashC = (msg) => hashCons().update(toBytes(msg)).digest();
    const tmp = hashCons();
    hashC.outputLen = tmp.outputLen;
    hashC.blockLen = tmp.blockLen;
    hashC.create = () => hashCons();
    return hashC;
  }
  function wrapXOFConstructorWithOpts(hashCons) {
    const hashC = (msg, opts) => hashCons(opts).update(toBytes(msg)).digest();
    const tmp = hashCons({});
    hashC.outputLen = tmp.outputLen;
    hashC.blockLen = tmp.blockLen;
    hashC.create = (opts) => hashCons(opts);
    return hashC;
  }
  function randomBytes(bytesLength = 32) {
    if (crypto && typeof crypto.getRandomValues === "function") {
      return crypto.getRandomValues(new Uint8Array(bytesLength));
    }
    throw new Error("crypto.getRandomValues must be defined");
  }

  // ../node_modules/@noble/hashes/esm/_md.js
  function setBigUint64(view, byteOffset, value, isLE2) {
    if (typeof view.setBigUint64 === "function")
      return view.setBigUint64(byteOffset, value, isLE2);
    const _32n2 = BigInt(32);
    const _u32_max = BigInt(4294967295);
    const wh = Number(value >> _32n2 & _u32_max);
    const wl = Number(value & _u32_max);
    const h = isLE2 ? 4 : 0;
    const l = isLE2 ? 0 : 4;
    view.setUint32(byteOffset + h, wh, isLE2);
    view.setUint32(byteOffset + l, wl, isLE2);
  }
  var Chi = (a, b, c) => a & b ^ ~a & c;
  var Maj = (a, b, c) => a & b ^ a & c ^ b & c;
  var HashMD = class extends Hash {
    constructor(blockLen, outputLen, padOffset, isLE2) {
      super();
      this.blockLen = blockLen;
      this.outputLen = outputLen;
      this.padOffset = padOffset;
      this.isLE = isLE2;
      this.finished = false;
      this.length = 0;
      this.pos = 0;
      this.destroyed = false;
      this.buffer = new Uint8Array(blockLen);
      this.view = createView(this.buffer);
    }
    update(data) {
      exists(this);
      const { view, buffer, blockLen } = this;
      data = toBytes(data);
      const len = data.length;
      for (let pos = 0; pos < len; ) {
        const take = Math.min(blockLen - this.pos, len - pos);
        if (take === blockLen) {
          const dataView = createView(data);
          for (; blockLen <= len - pos; pos += blockLen)
            this.process(dataView, pos);
          continue;
        }
        buffer.set(data.subarray(pos, pos + take), this.pos);
        this.pos += take;
        pos += take;
        if (this.pos === blockLen) {
          this.process(view, 0);
          this.pos = 0;
        }
      }
      this.length += data.length;
      this.roundClean();
      return this;
    }
    digestInto(out) {
      exists(this);
      output(out, this);
      this.finished = true;
      const { buffer, view, blockLen, isLE: isLE2 } = this;
      let { pos } = this;
      buffer[pos++] = 128;
      this.buffer.subarray(pos).fill(0);
      if (this.padOffset > blockLen - pos) {
        this.process(view, 0);
        pos = 0;
      }
      for (let i = pos; i < blockLen; i++)
        buffer[i] = 0;
      setBigUint64(view, blockLen - 8, BigInt(this.length * 8), isLE2);
      this.process(view, 0);
      const oview = createView(out);
      const len = this.outputLen;
      if (len % 4)
        throw new Error("_sha2: outputLen should be aligned to 32bit");
      const outLen = len / 4;
      const state = this.get();
      if (outLen > state.length)
        throw new Error("_sha2: outputLen bigger than state");
      for (let i = 0; i < outLen; i++)
        oview.setUint32(4 * i, state[i], isLE2);
    }
    digest() {
      const { buffer, outputLen } = this;
      this.digestInto(buffer);
      const res = buffer.slice(0, outputLen);
      this.destroy();
      return res;
    }
    _cloneInto(to) {
      to || (to = new this.constructor());
      to.set(...this.get());
      const { blockLen, buffer, length, finished, destroyed, pos } = this;
      to.length = length;
      to.pos = pos;
      to.finished = finished;
      to.destroyed = destroyed;
      if (length % blockLen)
        to.buffer.set(buffer);
      return to;
    }
  };

  // ../node_modules/@noble/hashes/esm/sha256.js
  var SHA256_K = /* @__PURE__ */ new Uint32Array([
    1116352408,
    1899447441,
    3049323471,
    3921009573,
    961987163,
    1508970993,
    2453635748,
    2870763221,
    3624381080,
    310598401,
    607225278,
    1426881987,
    1925078388,
    2162078206,
    2614888103,
    3248222580,
    3835390401,
    4022224774,
    264347078,
    604807628,
    770255983,
    1249150122,
    1555081692,
    1996064986,
    2554220882,
    2821834349,
    2952996808,
    3210313671,
    3336571891,
    3584528711,
    113926993,
    338241895,
    666307205,
    773529912,
    1294757372,
    1396182291,
    1695183700,
    1986661051,
    2177026350,
    2456956037,
    2730485921,
    2820302411,
    3259730800,
    3345764771,
    3516065817,
    3600352804,
    4094571909,
    275423344,
    430227734,
    506948616,
    659060556,
    883997877,
    958139571,
    1322822218,
    1537002063,
    1747873779,
    1955562222,
    2024104815,
    2227730452,
    2361852424,
    2428436474,
    2756734187,
    3204031479,
    3329325298
  ]);
  var SHA256_IV = /* @__PURE__ */ new Uint32Array([
    1779033703,
    3144134277,
    1013904242,
    2773480762,
    1359893119,
    2600822924,
    528734635,
    1541459225
  ]);
  var SHA256_W = /* @__PURE__ */ new Uint32Array(64);
  var SHA256 = class extends HashMD {
    constructor() {
      super(64, 32, 8, false);
      this.A = SHA256_IV[0] | 0;
      this.B = SHA256_IV[1] | 0;
      this.C = SHA256_IV[2] | 0;
      this.D = SHA256_IV[3] | 0;
      this.E = SHA256_IV[4] | 0;
      this.F = SHA256_IV[5] | 0;
      this.G = SHA256_IV[6] | 0;
      this.H = SHA256_IV[7] | 0;
    }
    get() {
      const { A, B, C, D, E, F, G, H } = this;
      return [A, B, C, D, E, F, G, H];
    }
    // prettier-ignore
    set(A, B, C, D, E, F, G, H) {
      this.A = A | 0;
      this.B = B | 0;
      this.C = C | 0;
      this.D = D | 0;
      this.E = E | 0;
      this.F = F | 0;
      this.G = G | 0;
      this.H = H | 0;
    }
    process(view, offset) {
      for (let i = 0; i < 16; i++, offset += 4)
        SHA256_W[i] = view.getUint32(offset, false);
      for (let i = 16; i < 64; i++) {
        const W15 = SHA256_W[i - 15];
        const W2 = SHA256_W[i - 2];
        const s0 = rotr(W15, 7) ^ rotr(W15, 18) ^ W15 >>> 3;
        const s1 = rotr(W2, 17) ^ rotr(W2, 19) ^ W2 >>> 10;
        SHA256_W[i] = s1 + SHA256_W[i - 7] + s0 + SHA256_W[i - 16] | 0;
      }
      let { A, B, C, D, E, F, G, H } = this;
      for (let i = 0; i < 64; i++) {
        const sigma1 = rotr(E, 6) ^ rotr(E, 11) ^ rotr(E, 25);
        const T1 = H + sigma1 + Chi(E, F, G) + SHA256_K[i] + SHA256_W[i] | 0;
        const sigma0 = rotr(A, 2) ^ rotr(A, 13) ^ rotr(A, 22);
        const T2 = sigma0 + Maj(A, B, C) | 0;
        H = G;
        G = F;
        F = E;
        E = D + T1 | 0;
        D = C;
        C = B;
        B = A;
        A = T1 + T2 | 0;
      }
      A = A + this.A | 0;
      B = B + this.B | 0;
      C = C + this.C | 0;
      D = D + this.D | 0;
      E = E + this.E | 0;
      F = F + this.F | 0;
      G = G + this.G | 0;
      H = H + this.H | 0;
      this.set(A, B, C, D, E, F, G, H);
    }
    roundClean() {
      SHA256_W.fill(0);
    }
    destroy() {
      this.set(0, 0, 0, 0, 0, 0, 0, 0);
      this.buffer.fill(0);
    }
  };
  var sha256 = /* @__PURE__ */ wrapConstructor(() => new SHA256());

  // ../esm/abstract/modular.js
  var _0n2 = BigInt(0);
  var _1n2 = BigInt(1);
  var _2n2 = BigInt(2);
  var _3n = BigInt(3);
  var _4n = BigInt(4);
  var _5n = BigInt(5);
  var _8n = BigInt(8);
  var _9n = BigInt(9);
  var _16n = BigInt(16);
  function mod(a, b) {
    const result = a % b;
    return result >= _0n2 ? result : b + result;
  }
  function pow(num, power, modulo) {
    if (modulo <= _0n2 || power < _0n2)
      throw new Error("Expected power/modulo > 0");
    if (modulo === _1n2)
      return _0n2;
    let res = _1n2;
    while (power > _0n2) {
      if (power & _1n2)
        res = res * num % modulo;
      num = num * num % modulo;
      power >>= _1n2;
    }
    return res;
  }
  function pow2(x, power, modulo) {
    let res = x;
    while (power-- > _0n2) {
      res *= res;
      res %= modulo;
    }
    return res;
  }
  function invert(number2, modulo) {
    if (number2 === _0n2 || modulo <= _0n2) {
      throw new Error(`invert: expected positive integers, got n=${number2} mod=${modulo}`);
    }
    let a = mod(number2, modulo);
    let b = modulo;
    let x = _0n2, y = _1n2, u = _1n2, v = _0n2;
    while (a !== _0n2) {
      const q = b / a;
      const r = b % a;
      const m = x - u * q;
      const n = y - v * q;
      b = a, a = r, x = u, y = v, u = m, v = n;
    }
    const gcd = b;
    if (gcd !== _1n2)
      throw new Error("invert: does not exist");
    return mod(x, modulo);
  }
  function tonelliShanks(P3) {
    const legendreC = (P3 - _1n2) / _2n2;
    let Q, S, Z;
    for (Q = P3 - _1n2, S = 0; Q % _2n2 === _0n2; Q /= _2n2, S++)
      ;
    for (Z = _2n2; Z < P3 && pow(Z, legendreC, P3) !== P3 - _1n2; Z++)
      ;
    if (S === 1) {
      const p1div4 = (P3 + _1n2) / _4n;
      return function tonelliFast(Fp8, n) {
        const root = Fp8.pow(n, p1div4);
        if (!Fp8.eql(Fp8.sqr(root), n))
          throw new Error("Cannot find square root");
        return root;
      };
    }
    const Q1div2 = (Q + _1n2) / _2n2;
    return function tonelliSlow(Fp8, n) {
      if (Fp8.pow(n, legendreC) === Fp8.neg(Fp8.ONE))
        throw new Error("Cannot find square root");
      let r = S;
      let g = Fp8.pow(Fp8.mul(Fp8.ONE, Z), Q);
      let x = Fp8.pow(n, Q1div2);
      let b = Fp8.pow(n, Q);
      while (!Fp8.eql(b, Fp8.ONE)) {
        if (Fp8.eql(b, Fp8.ZERO))
          return Fp8.ZERO;
        let m = 1;
        for (let t2 = Fp8.sqr(b); m < r; m++) {
          if (Fp8.eql(t2, Fp8.ONE))
            break;
          t2 = Fp8.sqr(t2);
        }
        const ge2 = Fp8.pow(g, _1n2 << BigInt(r - m - 1));
        g = Fp8.sqr(ge2);
        x = Fp8.mul(x, ge2);
        b = Fp8.mul(b, g);
        r = m;
      }
      return x;
    };
  }
  function FpSqrt(P3) {
    if (P3 % _4n === _3n) {
      const p1div4 = (P3 + _1n2) / _4n;
      return function sqrt3mod4(Fp8, n) {
        const root = Fp8.pow(n, p1div4);
        if (!Fp8.eql(Fp8.sqr(root), n))
          throw new Error("Cannot find square root");
        return root;
      };
    }
    if (P3 % _8n === _5n) {
      const c1 = (P3 - _5n) / _8n;
      return function sqrt5mod8(Fp8, n) {
        const n2 = Fp8.mul(n, _2n2);
        const v = Fp8.pow(n2, c1);
        const nv = Fp8.mul(n, v);
        const i = Fp8.mul(Fp8.mul(nv, _2n2), v);
        const root = Fp8.mul(nv, Fp8.sub(i, Fp8.ONE));
        if (!Fp8.eql(Fp8.sqr(root), n))
          throw new Error("Cannot find square root");
        return root;
      };
    }
    if (P3 % _16n === _9n) {
    }
    return tonelliShanks(P3);
  }
  var isNegativeLE = (num, modulo) => (mod(num, modulo) & _1n2) === _1n2;
  var FIELD_FIELDS = [
    "create",
    "isValid",
    "is0",
    "neg",
    "inv",
    "sqrt",
    "sqr",
    "eql",
    "add",
    "sub",
    "mul",
    "pow",
    "div",
    "addN",
    "subN",
    "mulN",
    "sqrN"
  ];
  function validateField(field) {
    const initial = {
      ORDER: "bigint",
      MASK: "bigint",
      BYTES: "isSafeInteger",
      BITS: "isSafeInteger"
    };
    const opts = FIELD_FIELDS.reduce((map, val) => {
      map[val] = "function";
      return map;
    }, initial);
    return validateObject(field, opts);
  }
  function FpPow(f, num, power) {
    if (power < _0n2)
      throw new Error("Expected power > 0");
    if (power === _0n2)
      return f.ONE;
    if (power === _1n2)
      return num;
    let p = f.ONE;
    let d = num;
    while (power > _0n2) {
      if (power & _1n2)
        p = f.mul(p, d);
      d = f.sqr(d);
      power >>= _1n2;
    }
    return p;
  }
  function FpInvertBatch(f, nums) {
    const tmp = new Array(nums.length);
    const lastMultiplied = nums.reduce((acc, num, i) => {
      if (f.is0(num))
        return acc;
      tmp[i] = acc;
      return f.mul(acc, num);
    }, f.ONE);
    const inverted = f.inv(lastMultiplied);
    nums.reduceRight((acc, num, i) => {
      if (f.is0(num))
        return acc;
      tmp[i] = f.mul(acc, tmp[i]);
      return f.mul(acc, num);
    }, inverted);
    return tmp;
  }
  function nLength(n, nBitLength) {
    const _nBitLength = nBitLength !== void 0 ? nBitLength : n.toString(2).length;
    const nByteLength = Math.ceil(_nBitLength / 8);
    return { nBitLength: _nBitLength, nByteLength };
  }
  function Field(ORDER, bitLen2, isLE2 = false, redef = {}) {
    if (ORDER <= _0n2)
      throw new Error(`Expected Field ORDER > 0, got ${ORDER}`);
    const { nBitLength: BITS, nByteLength: BYTES } = nLength(ORDER, bitLen2);
    if (BYTES > 2048)
      throw new Error("Field lengths over 2048 bytes are not supported");
    const sqrtP = FpSqrt(ORDER);
    const f = Object.freeze({
      ORDER,
      BITS,
      BYTES,
      MASK: bitMask(BITS),
      ZERO: _0n2,
      ONE: _1n2,
      create: (num) => mod(num, ORDER),
      isValid: (num) => {
        if (typeof num !== "bigint")
          throw new Error(`Invalid field element: expected bigint, got ${typeof num}`);
        return _0n2 <= num && num < ORDER;
      },
      is0: (num) => num === _0n2,
      isOdd: (num) => (num & _1n2) === _1n2,
      neg: (num) => mod(-num, ORDER),
      eql: (lhs, rhs) => lhs === rhs,
      sqr: (num) => mod(num * num, ORDER),
      add: (lhs, rhs) => mod(lhs + rhs, ORDER),
      sub: (lhs, rhs) => mod(lhs - rhs, ORDER),
      mul: (lhs, rhs) => mod(lhs * rhs, ORDER),
      pow: (num, power) => FpPow(f, num, power),
      div: (lhs, rhs) => mod(lhs * invert(rhs, ORDER), ORDER),
      // Same as above, but doesn't normalize
      sqrN: (num) => num * num,
      addN: (lhs, rhs) => lhs + rhs,
      subN: (lhs, rhs) => lhs - rhs,
      mulN: (lhs, rhs) => lhs * rhs,
      inv: (num) => invert(num, ORDER),
      sqrt: redef.sqrt || ((n) => sqrtP(f, n)),
      invertBatch: (lst) => FpInvertBatch(f, lst),
      // TODO: do we really need constant cmov?
      // We don't have const-time bigints anyway, so probably will be not very useful
      cmov: (a, b, c) => c ? b : a,
      toBytes: (num) => isLE2 ? numberToBytesLE(num, BYTES) : numberToBytesBE(num, BYTES),
      fromBytes: (bytes2) => {
        if (bytes2.length !== BYTES)
          throw new Error(`Fp.fromBytes: expected ${BYTES}, got ${bytes2.length}`);
        return isLE2 ? bytesToNumberLE(bytes2) : bytesToNumberBE(bytes2);
      }
    });
    return Object.freeze(f);
  }
  function FpSqrtEven(Fp8, elm) {
    if (!Fp8.isOdd)
      throw new Error(`Field doesn't have isOdd`);
    const root = Fp8.sqrt(elm);
    return Fp8.isOdd(root) ? Fp8.neg(root) : root;
  }
  function getFieldBytesLength(fieldOrder) {
    if (typeof fieldOrder !== "bigint")
      throw new Error("field order must be bigint");
    const bitLength = fieldOrder.toString(2).length;
    return Math.ceil(bitLength / 8);
  }
  function getMinHashLength(fieldOrder) {
    const length = getFieldBytesLength(fieldOrder);
    return length + Math.ceil(length / 2);
  }
  function mapHashToField(key, fieldOrder, isLE2 = false) {
    const len = key.length;
    const fieldLen = getFieldBytesLength(fieldOrder);
    const minLen = getMinHashLength(fieldOrder);
    if (len < 16 || len < minLen || len > 1024)
      throw new Error(`expected ${minLen}-1024 bytes of input, got ${len}`);
    const num = isLE2 ? bytesToNumberBE(key) : bytesToNumberLE(key);
    const reduced = mod(num, fieldOrder - _1n2) + _1n2;
    return isLE2 ? numberToBytesLE(reduced, fieldLen) : numberToBytesBE(reduced, fieldLen);
  }

  // ../esm/abstract/curve.js
  var _0n3 = BigInt(0);
  var _1n3 = BigInt(1);
  function wNAF(c, bits) {
    const constTimeNegate = (condition, item) => {
      const neg = item.negate();
      return condition ? neg : item;
    };
    const opts = (W) => {
      const windows = Math.ceil(bits / W) + 1;
      const windowSize = 2 ** (W - 1);
      return { windows, windowSize };
    };
    return {
      constTimeNegate,
      // non-const time multiplication ladder
      unsafeLadder(elm, n) {
        let p = c.ZERO;
        let d = elm;
        while (n > _0n3) {
          if (n & _1n3)
            p = p.add(d);
          d = d.double();
          n >>= _1n3;
        }
        return p;
      },
      /**
       * Creates a wNAF precomputation window. Used for caching.
       * Default window size is set by `utils.precompute()` and is equal to 8.
       * Number of precomputed points depends on the curve size:
       * 2^(𝑊−1) * (Math.ceil(𝑛 / 𝑊) + 1), where:
       * - 𝑊 is the window size
       * - 𝑛 is the bitlength of the curve order.
       * For a 256-bit curve and window size 8, the number of precomputed points is 128 * 33 = 4224.
       * @returns precomputed point tables flattened to a single array
       */
      precomputeWindow(elm, W) {
        const { windows, windowSize } = opts(W);
        const points = [];
        let p = elm;
        let base = p;
        for (let window = 0; window < windows; window++) {
          base = p;
          points.push(base);
          for (let i = 1; i < windowSize; i++) {
            base = base.add(p);
            points.push(base);
          }
          p = base.double();
        }
        return points;
      },
      /**
       * Implements ec multiplication using precomputed tables and w-ary non-adjacent form.
       * @param W window size
       * @param precomputes precomputed tables
       * @param n scalar (we don't check here, but should be less than curve order)
       * @returns real and fake (for const-time) points
       */
      wNAF(W, precomputes, n) {
        const { windows, windowSize } = opts(W);
        let p = c.ZERO;
        let f = c.BASE;
        const mask = BigInt(2 ** W - 1);
        const maxNumber = 2 ** W;
        const shiftBy = BigInt(W);
        for (let window = 0; window < windows; window++) {
          const offset = window * windowSize;
          let wbits = Number(n & mask);
          n >>= shiftBy;
          if (wbits > windowSize) {
            wbits -= maxNumber;
            n += _1n3;
          }
          const offset1 = offset;
          const offset2 = offset + Math.abs(wbits) - 1;
          const cond1 = window % 2 !== 0;
          const cond2 = wbits < 0;
          if (wbits === 0) {
            f = f.add(constTimeNegate(cond1, precomputes[offset1]));
          } else {
            p = p.add(constTimeNegate(cond2, precomputes[offset2]));
          }
        }
        return { p, f };
      },
      wNAFCached(P3, precomputesMap, n, transform) {
        const W = P3._WINDOW_SIZE || 1;
        let comp = precomputesMap.get(P3);
        if (!comp) {
          comp = this.precomputeWindow(P3, W);
          if (W !== 1) {
            precomputesMap.set(P3, transform(comp));
          }
        }
        return this.wNAF(W, comp, n);
      }
    };
  }
  function validateBasic(curve) {
    validateField(curve.Fp);
    validateObject(curve, {
      n: "bigint",
      h: "bigint",
      Gx: "field",
      Gy: "field"
    }, {
      nBitLength: "isSafeInteger",
      nByteLength: "isSafeInteger"
    });
    return Object.freeze({
      ...nLength(curve.n, curve.nBitLength),
      ...curve,
      ...{ p: curve.Fp.ORDER }
    });
  }

  // ../esm/abstract/weierstrass.js
  function validatePointOpts(curve) {
    const opts = validateBasic(curve);
    validateObject(opts, {
      a: "field",
      b: "field"
    }, {
      allowedPrivateKeyLengths: "array",
      wrapPrivateKey: "boolean",
      isTorsionFree: "function",
      clearCofactor: "function",
      allowInfinityPoint: "boolean",
      fromBytes: "function",
      toBytes: "function"
    });
    const { endo, Fp: Fp8, a } = opts;
    if (endo) {
      if (!Fp8.eql(a, Fp8.ZERO)) {
        throw new Error("Endomorphism can only be defined for Koblitz curves that have a=0");
      }
      if (typeof endo !== "object" || typeof endo.beta !== "bigint" || typeof endo.splitScalar !== "function") {
        throw new Error("Expected endomorphism with beta: bigint and splitScalar: function");
      }
    }
    return Object.freeze({ ...opts });
  }
  var { bytesToNumberBE: b2n, hexToBytes: h2b } = utils_exports;
  var DER = {
    // asn.1 DER encoding utils
    Err: class DERErr extends Error {
      constructor(m = "") {
        super(m);
      }
    },
    _parseInt(data) {
      const { Err: E } = DER;
      if (data.length < 2 || data[0] !== 2)
        throw new E("Invalid signature integer tag");
      const len = data[1];
      const res = data.subarray(2, len + 2);
      if (!len || res.length !== len)
        throw new E("Invalid signature integer: wrong length");
      if (res[0] & 128)
        throw new E("Invalid signature integer: negative");
      if (res[0] === 0 && !(res[1] & 128))
        throw new E("Invalid signature integer: unnecessary leading zero");
      return { d: b2n(res), l: data.subarray(len + 2) };
    },
    toSig(hex) {
      const { Err: E } = DER;
      const data = typeof hex === "string" ? h2b(hex) : hex;
      abytes(data);
      let l = data.length;
      if (l < 2 || data[0] != 48)
        throw new E("Invalid signature tag");
      if (data[1] !== l - 2)
        throw new E("Invalid signature: incorrect length");
      const { d: r, l: sBytes } = DER._parseInt(data.subarray(2));
      const { d: s, l: rBytesLeft } = DER._parseInt(sBytes);
      if (rBytesLeft.length)
        throw new E("Invalid signature: left bytes after parsing");
      return { r, s };
    },
    hexFromSig(sig) {
      const slice = (s2) => Number.parseInt(s2[0], 16) & 8 ? "00" + s2 : s2;
      const h = (num) => {
        const hex = num.toString(16);
        return hex.length & 1 ? `0${hex}` : hex;
      };
      const s = slice(h(sig.s));
      const r = slice(h(sig.r));
      const shl = s.length / 2;
      const rhl = r.length / 2;
      const sl = h(shl);
      const rl = h(rhl);
      return `30${h(rhl + shl + 4)}02${rl}${r}02${sl}${s}`;
    }
  };
  var _0n4 = BigInt(0);
  var _1n4 = BigInt(1);
  var _2n3 = BigInt(2);
  var _3n2 = BigInt(3);
  var _4n2 = BigInt(4);
  function weierstrassPoints(opts) {
    const CURVE2 = validatePointOpts(opts);
    const { Fp: Fp8 } = CURVE2;
    const toBytes2 = CURVE2.toBytes || ((_c, point, _isCompressed) => {
      const a = point.toAffine();
      return concatBytes(Uint8Array.from([4]), Fp8.toBytes(a.x), Fp8.toBytes(a.y));
    });
    const fromBytes = CURVE2.fromBytes || ((bytes2) => {
      const tail = bytes2.subarray(1);
      const x = Fp8.fromBytes(tail.subarray(0, Fp8.BYTES));
      const y = Fp8.fromBytes(tail.subarray(Fp8.BYTES, 2 * Fp8.BYTES));
      return { x, y };
    });
    function weierstrassEquation(x) {
      const { a, b } = CURVE2;
      const x2 = Fp8.sqr(x);
      const x3 = Fp8.mul(x2, x);
      return Fp8.add(Fp8.add(x3, Fp8.mul(x, a)), b);
    }
    if (!Fp8.eql(Fp8.sqr(CURVE2.Gy), weierstrassEquation(CURVE2.Gx)))
      throw new Error("bad generator point: equation left != right");
    function isWithinCurveOrder(num) {
      return typeof num === "bigint" && _0n4 < num && num < CURVE2.n;
    }
    function assertGE(num) {
      if (!isWithinCurveOrder(num))
        throw new Error("Expected valid bigint: 0 < bigint < curve.n");
    }
    function normPrivateKeyToScalar(key) {
      const { allowedPrivateKeyLengths: lengths, nByteLength, wrapPrivateKey, n } = CURVE2;
      if (lengths && typeof key !== "bigint") {
        if (isBytes(key))
          key = bytesToHex(key);
        if (typeof key !== "string" || !lengths.includes(key.length))
          throw new Error("Invalid key");
        key = key.padStart(nByteLength * 2, "0");
      }
      let num;
      try {
        num = typeof key === "bigint" ? key : bytesToNumberBE(ensureBytes("private key", key, nByteLength));
      } catch (error) {
        throw new Error(`private key must be ${nByteLength} bytes, hex or bigint, not ${typeof key}`);
      }
      if (wrapPrivateKey)
        num = mod(num, n);
      assertGE(num);
      return num;
    }
    const pointPrecomputes = /* @__PURE__ */ new Map();
    function assertPrjPoint(other) {
      if (!(other instanceof Point2))
        throw new Error("ProjectivePoint expected");
    }
    class Point2 {
      constructor(px, py, pz) {
        this.px = px;
        this.py = py;
        this.pz = pz;
        if (px == null || !Fp8.isValid(px))
          throw new Error("x required");
        if (py == null || !Fp8.isValid(py))
          throw new Error("y required");
        if (pz == null || !Fp8.isValid(pz))
          throw new Error("z required");
      }
      // Does not validate if the point is on-curve.
      // Use fromHex instead, or call assertValidity() later.
      static fromAffine(p) {
        const { x, y } = p || {};
        if (!p || !Fp8.isValid(x) || !Fp8.isValid(y))
          throw new Error("invalid affine point");
        if (p instanceof Point2)
          throw new Error("projective point not allowed");
        const is0 = (i) => Fp8.eql(i, Fp8.ZERO);
        if (is0(x) && is0(y))
          return Point2.ZERO;
        return new Point2(x, y, Fp8.ONE);
      }
      get x() {
        return this.toAffine().x;
      }
      get y() {
        return this.toAffine().y;
      }
      /**
       * Takes a bunch of Projective Points but executes only one
       * inversion on all of them. Inversion is very slow operation,
       * so this improves performance massively.
       * Optimization: converts a list of projective points to a list of identical points with Z=1.
       */
      static normalizeZ(points) {
        const toInv = Fp8.invertBatch(points.map((p) => p.pz));
        return points.map((p, i) => p.toAffine(toInv[i])).map(Point2.fromAffine);
      }
      /**
       * Converts hash string or Uint8Array to Point.
       * @param hex short/long ECDSA hex
       */
      static fromHex(hex) {
        const P3 = Point2.fromAffine(fromBytes(ensureBytes("pointHex", hex)));
        P3.assertValidity();
        return P3;
      }
      // Multiplies generator point by privateKey.
      static fromPrivateKey(privateKey) {
        return Point2.BASE.multiply(normPrivateKeyToScalar(privateKey));
      }
      // "Private method", don't use it directly
      _setWindowSize(windowSize) {
        this._WINDOW_SIZE = windowSize;
        pointPrecomputes.delete(this);
      }
      // A point on curve is valid if it conforms to equation.
      assertValidity() {
        if (this.is0()) {
          if (CURVE2.allowInfinityPoint && !Fp8.is0(this.py))
            return;
          throw new Error("bad point: ZERO");
        }
        const { x, y } = this.toAffine();
        if (!Fp8.isValid(x) || !Fp8.isValid(y))
          throw new Error("bad point: x or y not FE");
        const left = Fp8.sqr(y);
        const right = weierstrassEquation(x);
        if (!Fp8.eql(left, right))
          throw new Error("bad point: equation left != right");
        if (!this.isTorsionFree())
          throw new Error("bad point: not in prime-order subgroup");
      }
      hasEvenY() {
        const { y } = this.toAffine();
        if (Fp8.isOdd)
          return !Fp8.isOdd(y);
        throw new Error("Field doesn't support isOdd");
      }
      /**
       * Compare one point to another.
       */
      equals(other) {
        assertPrjPoint(other);
        const { px: X1, py: Y1, pz: Z1 } = this;
        const { px: X2, py: Y2, pz: Z2 } = other;
        const U1 = Fp8.eql(Fp8.mul(X1, Z2), Fp8.mul(X2, Z1));
        const U2 = Fp8.eql(Fp8.mul(Y1, Z2), Fp8.mul(Y2, Z1));
        return U1 && U2;
      }
      /**
       * Flips point to one corresponding to (x, -y) in Affine coordinates.
       */
      negate() {
        return new Point2(this.px, Fp8.neg(this.py), this.pz);
      }
      // Renes-Costello-Batina exception-free doubling formula.
      // There is 30% faster Jacobian formula, but it is not complete.
      // https://eprint.iacr.org/2015/1060, algorithm 3
      // Cost: 8M + 3S + 3*a + 2*b3 + 15add.
      double() {
        const { a, b } = CURVE2;
        const b3 = Fp8.mul(b, _3n2);
        const { px: X1, py: Y1, pz: Z1 } = this;
        let X3 = Fp8.ZERO, Y3 = Fp8.ZERO, Z3 = Fp8.ZERO;
        let t0 = Fp8.mul(X1, X1);
        let t1 = Fp8.mul(Y1, Y1);
        let t2 = Fp8.mul(Z1, Z1);
        let t3 = Fp8.mul(X1, Y1);
        t3 = Fp8.add(t3, t3);
        Z3 = Fp8.mul(X1, Z1);
        Z3 = Fp8.add(Z3, Z3);
        X3 = Fp8.mul(a, Z3);
        Y3 = Fp8.mul(b3, t2);
        Y3 = Fp8.add(X3, Y3);
        X3 = Fp8.sub(t1, Y3);
        Y3 = Fp8.add(t1, Y3);
        Y3 = Fp8.mul(X3, Y3);
        X3 = Fp8.mul(t3, X3);
        Z3 = Fp8.mul(b3, Z3);
        t2 = Fp8.mul(a, t2);
        t3 = Fp8.sub(t0, t2);
        t3 = Fp8.mul(a, t3);
        t3 = Fp8.add(t3, Z3);
        Z3 = Fp8.add(t0, t0);
        t0 = Fp8.add(Z3, t0);
        t0 = Fp8.add(t0, t2);
        t0 = Fp8.mul(t0, t3);
        Y3 = Fp8.add(Y3, t0);
        t2 = Fp8.mul(Y1, Z1);
        t2 = Fp8.add(t2, t2);
        t0 = Fp8.mul(t2, t3);
        X3 = Fp8.sub(X3, t0);
        Z3 = Fp8.mul(t2, t1);
        Z3 = Fp8.add(Z3, Z3);
        Z3 = Fp8.add(Z3, Z3);
        return new Point2(X3, Y3, Z3);
      }
      // Renes-Costello-Batina exception-free addition formula.
      // There is 30% faster Jacobian formula, but it is not complete.
      // https://eprint.iacr.org/2015/1060, algorithm 1
      // Cost: 12M + 0S + 3*a + 3*b3 + 23add.
      add(other) {
        assertPrjPoint(other);
        const { px: X1, py: Y1, pz: Z1 } = this;
        const { px: X2, py: Y2, pz: Z2 } = other;
        let X3 = Fp8.ZERO, Y3 = Fp8.ZERO, Z3 = Fp8.ZERO;
        const a = CURVE2.a;
        const b3 = Fp8.mul(CURVE2.b, _3n2);
        let t0 = Fp8.mul(X1, X2);
        let t1 = Fp8.mul(Y1, Y2);
        let t2 = Fp8.mul(Z1, Z2);
        let t3 = Fp8.add(X1, Y1);
        let t4 = Fp8.add(X2, Y2);
        t3 = Fp8.mul(t3, t4);
        t4 = Fp8.add(t0, t1);
        t3 = Fp8.sub(t3, t4);
        t4 = Fp8.add(X1, Z1);
        let t5 = Fp8.add(X2, Z2);
        t4 = Fp8.mul(t4, t5);
        t5 = Fp8.add(t0, t2);
        t4 = Fp8.sub(t4, t5);
        t5 = Fp8.add(Y1, Z1);
        X3 = Fp8.add(Y2, Z2);
        t5 = Fp8.mul(t5, X3);
        X3 = Fp8.add(t1, t2);
        t5 = Fp8.sub(t5, X3);
        Z3 = Fp8.mul(a, t4);
        X3 = Fp8.mul(b3, t2);
        Z3 = Fp8.add(X3, Z3);
        X3 = Fp8.sub(t1, Z3);
        Z3 = Fp8.add(t1, Z3);
        Y3 = Fp8.mul(X3, Z3);
        t1 = Fp8.add(t0, t0);
        t1 = Fp8.add(t1, t0);
        t2 = Fp8.mul(a, t2);
        t4 = Fp8.mul(b3, t4);
        t1 = Fp8.add(t1, t2);
        t2 = Fp8.sub(t0, t2);
        t2 = Fp8.mul(a, t2);
        t4 = Fp8.add(t4, t2);
        t0 = Fp8.mul(t1, t4);
        Y3 = Fp8.add(Y3, t0);
        t0 = Fp8.mul(t5, t4);
        X3 = Fp8.mul(t3, X3);
        X3 = Fp8.sub(X3, t0);
        t0 = Fp8.mul(t3, t1);
        Z3 = Fp8.mul(t5, Z3);
        Z3 = Fp8.add(Z3, t0);
        return new Point2(X3, Y3, Z3);
      }
      subtract(other) {
        return this.add(other.negate());
      }
      is0() {
        return this.equals(Point2.ZERO);
      }
      wNAF(n) {
        return wnaf.wNAFCached(this, pointPrecomputes, n, (comp) => {
          const toInv = Fp8.invertBatch(comp.map((p) => p.pz));
          return comp.map((p, i) => p.toAffine(toInv[i])).map(Point2.fromAffine);
        });
      }
      /**
       * Non-constant-time multiplication. Uses double-and-add algorithm.
       * It's faster, but should only be used when you don't care about
       * an exposed private key e.g. sig verification, which works over *public* keys.
       */
      multiplyUnsafe(n) {
        const I = Point2.ZERO;
        if (n === _0n4)
          return I;
        assertGE(n);
        if (n === _1n4)
          return this;
        const { endo } = CURVE2;
        if (!endo)
          return wnaf.unsafeLadder(this, n);
        let { k1neg, k1, k2neg, k2 } = endo.splitScalar(n);
        let k1p = I;
        let k2p = I;
        let d = this;
        while (k1 > _0n4 || k2 > _0n4) {
          if (k1 & _1n4)
            k1p = k1p.add(d);
          if (k2 & _1n4)
            k2p = k2p.add(d);
          d = d.double();
          k1 >>= _1n4;
          k2 >>= _1n4;
        }
        if (k1neg)
          k1p = k1p.negate();
        if (k2neg)
          k2p = k2p.negate();
        k2p = new Point2(Fp8.mul(k2p.px, endo.beta), k2p.py, k2p.pz);
        return k1p.add(k2p);
      }
      /**
       * Constant time multiplication.
       * Uses wNAF method. Windowed method may be 10% faster,
       * but takes 2x longer to generate and consumes 2x memory.
       * Uses precomputes when available.
       * Uses endomorphism for Koblitz curves.
       * @param scalar by which the point would be multiplied
       * @returns New point
       */
      multiply(scalar) {
        assertGE(scalar);
        let n = scalar;
        let point, fake;
        const { endo } = CURVE2;
        if (endo) {
          const { k1neg, k1, k2neg, k2 } = endo.splitScalar(n);
          let { p: k1p, f: f1p } = this.wNAF(k1);
          let { p: k2p, f: f2p } = this.wNAF(k2);
          k1p = wnaf.constTimeNegate(k1neg, k1p);
          k2p = wnaf.constTimeNegate(k2neg, k2p);
          k2p = new Point2(Fp8.mul(k2p.px, endo.beta), k2p.py, k2p.pz);
          point = k1p.add(k2p);
          fake = f1p.add(f2p);
        } else {
          const { p, f } = this.wNAF(n);
          point = p;
          fake = f;
        }
        return Point2.normalizeZ([point, fake])[0];
      }
      /**
       * Efficiently calculate `aP + bQ`. Unsafe, can expose private key, if used incorrectly.
       * Not using Strauss-Shamir trick: precomputation tables are faster.
       * The trick could be useful if both P and Q are not G (not in our case).
       * @returns non-zero affine point
       */
      multiplyAndAddUnsafe(Q, a, b) {
        const G = Point2.BASE;
        const mul = (P3, a2) => a2 === _0n4 || a2 === _1n4 || !P3.equals(G) ? P3.multiplyUnsafe(a2) : P3.multiply(a2);
        const sum = mul(this, a).add(mul(Q, b));
        return sum.is0() ? void 0 : sum;
      }
      // Converts Projective point to affine (x, y) coordinates.
      // Can accept precomputed Z^-1 - for example, from invertBatch.
      // (x, y, z) ∋ (x=x/z, y=y/z)
      toAffine(iz) {
        const { px: x, py: y, pz: z } = this;
        const is0 = this.is0();
        if (iz == null)
          iz = is0 ? Fp8.ONE : Fp8.inv(z);
        const ax = Fp8.mul(x, iz);
        const ay = Fp8.mul(y, iz);
        const zz = Fp8.mul(z, iz);
        if (is0)
          return { x: Fp8.ZERO, y: Fp8.ZERO };
        if (!Fp8.eql(zz, Fp8.ONE))
          throw new Error("invZ was invalid");
        return { x: ax, y: ay };
      }
      isTorsionFree() {
        const { h: cofactor, isTorsionFree } = CURVE2;
        if (cofactor === _1n4)
          return true;
        if (isTorsionFree)
          return isTorsionFree(Point2, this);
        throw new Error("isTorsionFree() has not been declared for the elliptic curve");
      }
      clearCofactor() {
        const { h: cofactor, clearCofactor } = CURVE2;
        if (cofactor === _1n4)
          return this;
        if (clearCofactor)
          return clearCofactor(Point2, this);
        return this.multiplyUnsafe(CURVE2.h);
      }
      toRawBytes(isCompressed = true) {
        this.assertValidity();
        return toBytes2(Point2, this, isCompressed);
      }
      toHex(isCompressed = true) {
        return bytesToHex(this.toRawBytes(isCompressed));
      }
    }
    Point2.BASE = new Point2(CURVE2.Gx, CURVE2.Gy, Fp8.ONE);
    Point2.ZERO = new Point2(Fp8.ZERO, Fp8.ONE, Fp8.ZERO);
    const _bits = CURVE2.nBitLength;
    const wnaf = wNAF(Point2, CURVE2.endo ? Math.ceil(_bits / 2) : _bits);
    return {
      CURVE: CURVE2,
      ProjectivePoint: Point2,
      normPrivateKeyToScalar,
      weierstrassEquation,
      isWithinCurveOrder
    };
  }
  function validateOpts(curve) {
    const opts = validateBasic(curve);
    validateObject(opts, {
      hash: "hash",
      hmac: "function",
      randomBytes: "function"
    }, {
      bits2int: "function",
      bits2int_modN: "function",
      lowS: "boolean"
    });
    return Object.freeze({ lowS: true, ...opts });
  }
  function weierstrass(curveDef) {
    const CURVE2 = validateOpts(curveDef);
    const { Fp: Fp8, n: CURVE_ORDER } = CURVE2;
    const compressedLen = Fp8.BYTES + 1;
    const uncompressedLen = 2 * Fp8.BYTES + 1;
    function isValidFieldElement(num) {
      return _0n4 < num && num < Fp8.ORDER;
    }
    function modN2(a) {
      return mod(a, CURVE_ORDER);
    }
    function invN(a) {
      return invert(a, CURVE_ORDER);
    }
    const { ProjectivePoint: Point2, normPrivateKeyToScalar, weierstrassEquation, isWithinCurveOrder } = weierstrassPoints({
      ...CURVE2,
      toBytes(_c, point, isCompressed) {
        const a = point.toAffine();
        const x = Fp8.toBytes(a.x);
        const cat = concatBytes;
        if (isCompressed) {
          return cat(Uint8Array.from([point.hasEvenY() ? 2 : 3]), x);
        } else {
          return cat(Uint8Array.from([4]), x, Fp8.toBytes(a.y));
        }
      },
      fromBytes(bytes2) {
        const len = bytes2.length;
        const head = bytes2[0];
        const tail = bytes2.subarray(1);
        if (len === compressedLen && (head === 2 || head === 3)) {
          const x = bytesToNumberBE(tail);
          if (!isValidFieldElement(x))
            throw new Error("Point is not on curve");
          const y2 = weierstrassEquation(x);
          let y;
          try {
            y = Fp8.sqrt(y2);
          } catch (sqrtError) {
            const suffix = sqrtError instanceof Error ? ": " + sqrtError.message : "";
            throw new Error("Point is not on curve" + suffix);
          }
          const isYOdd = (y & _1n4) === _1n4;
          const isHeadOdd = (head & 1) === 1;
          if (isHeadOdd !== isYOdd)
            y = Fp8.neg(y);
          return { x, y };
        } else if (len === uncompressedLen && head === 4) {
          const x = Fp8.fromBytes(tail.subarray(0, Fp8.BYTES));
          const y = Fp8.fromBytes(tail.subarray(Fp8.BYTES, 2 * Fp8.BYTES));
          return { x, y };
        } else {
          throw new Error(`Point of length ${len} was invalid. Expected ${compressedLen} compressed bytes or ${uncompressedLen} uncompressed bytes`);
        }
      }
    });
    const numToNByteStr = (num) => bytesToHex(numberToBytesBE(num, CURVE2.nByteLength));
    function isBiggerThanHalfOrder(number2) {
      const HALF = CURVE_ORDER >> _1n4;
      return number2 > HALF;
    }
    function normalizeS(s) {
      return isBiggerThanHalfOrder(s) ? modN2(-s) : s;
    }
    const slcNum = (b, from, to) => bytesToNumberBE(b.slice(from, to));
    class Signature {
      constructor(r, s, recovery) {
        this.r = r;
        this.s = s;
        this.recovery = recovery;
        this.assertValidity();
      }
      // pair (bytes of r, bytes of s)
      static fromCompact(hex) {
        const l = CURVE2.nByteLength;
        hex = ensureBytes("compactSignature", hex, l * 2);
        return new Signature(slcNum(hex, 0, l), slcNum(hex, l, 2 * l));
      }
      // DER encoded ECDSA signature
      // https://bitcoin.stackexchange.com/questions/57644/what-are-the-parts-of-a-bitcoin-transaction-input-script
      static fromDER(hex) {
        const { r, s } = DER.toSig(ensureBytes("DER", hex));
        return new Signature(r, s);
      }
      assertValidity() {
        if (!isWithinCurveOrder(this.r))
          throw new Error("r must be 0 < r < CURVE.n");
        if (!isWithinCurveOrder(this.s))
          throw new Error("s must be 0 < s < CURVE.n");
      }
      addRecoveryBit(recovery) {
        return new Signature(this.r, this.s, recovery);
      }
      recoverPublicKey(msgHash) {
        const { r, s, recovery: rec } = this;
        const h = bits2int_modN(ensureBytes("msgHash", msgHash));
        if (rec == null || ![0, 1, 2, 3].includes(rec))
          throw new Error("recovery id invalid");
        const radj = rec === 2 || rec === 3 ? r + CURVE2.n : r;
        if (radj >= Fp8.ORDER)
          throw new Error("recovery id 2 or 3 invalid");
        const prefix = (rec & 1) === 0 ? "02" : "03";
        const R = Point2.fromHex(prefix + numToNByteStr(radj));
        const ir = invN(radj);
        const u1 = modN2(-h * ir);
        const u2 = modN2(s * ir);
        const Q = Point2.BASE.multiplyAndAddUnsafe(R, u1, u2);
        if (!Q)
          throw new Error("point at infinify");
        Q.assertValidity();
        return Q;
      }
      // Signatures should be low-s, to prevent malleability.
      hasHighS() {
        return isBiggerThanHalfOrder(this.s);
      }
      normalizeS() {
        return this.hasHighS() ? new Signature(this.r, modN2(-this.s), this.recovery) : this;
      }
      // DER-encoded
      toDERRawBytes() {
        return hexToBytes(this.toDERHex());
      }
      toDERHex() {
        return DER.hexFromSig({ r: this.r, s: this.s });
      }
      // padded bytes of r, then padded bytes of s
      toCompactRawBytes() {
        return hexToBytes(this.toCompactHex());
      }
      toCompactHex() {
        return numToNByteStr(this.r) + numToNByteStr(this.s);
      }
    }
    const utils2 = {
      isValidPrivateKey(privateKey) {
        try {
          normPrivateKeyToScalar(privateKey);
          return true;
        } catch (error) {
          return false;
        }
      },
      normPrivateKeyToScalar,
      /**
       * Produces cryptographically secure private key from random of size
       * (groupLen + ceil(groupLen / 2)) with modulo bias being negligible.
       */
      randomPrivateKey: () => {
        const length = getMinHashLength(CURVE2.n);
        return mapHashToField(CURVE2.randomBytes(length), CURVE2.n);
      },
      /**
       * Creates precompute table for an arbitrary EC point. Makes point "cached".
       * Allows to massively speed-up `point.multiply(scalar)`.
       * @returns cached point
       * @example
       * const fast = utils.precompute(8, ProjectivePoint.fromHex(someonesPubKey));
       * fast.multiply(privKey); // much faster ECDH now
       */
      precompute(windowSize = 8, point = Point2.BASE) {
        point._setWindowSize(windowSize);
        point.multiply(BigInt(3));
        return point;
      }
    };
    function getPublicKey(privateKey, isCompressed = true) {
      return Point2.fromPrivateKey(privateKey).toRawBytes(isCompressed);
    }
    function isProbPub(item) {
      const arr = isBytes(item);
      const str = typeof item === "string";
      const len = (arr || str) && item.length;
      if (arr)
        return len === compressedLen || len === uncompressedLen;
      if (str)
        return len === 2 * compressedLen || len === 2 * uncompressedLen;
      if (item instanceof Point2)
        return true;
      return false;
    }
    function getSharedSecret(privateA, publicB, isCompressed = true) {
      if (isProbPub(privateA))
        throw new Error("first arg must be private key");
      if (!isProbPub(publicB))
        throw new Error("second arg must be public key");
      const b = Point2.fromHex(publicB);
      return b.multiply(normPrivateKeyToScalar(privateA)).toRawBytes(isCompressed);
    }
    const bits2int = CURVE2.bits2int || function(bytes2) {
      const num = bytesToNumberBE(bytes2);
      const delta = bytes2.length * 8 - CURVE2.nBitLength;
      return delta > 0 ? num >> BigInt(delta) : num;
    };
    const bits2int_modN = CURVE2.bits2int_modN || function(bytes2) {
      return modN2(bits2int(bytes2));
    };
    const ORDER_MASK = bitMask(CURVE2.nBitLength);
    function int2octets(num) {
      if (typeof num !== "bigint")
        throw new Error("bigint expected");
      if (!(_0n4 <= num && num < ORDER_MASK))
        throw new Error(`bigint expected < 2^${CURVE2.nBitLength}`);
      return numberToBytesBE(num, CURVE2.nByteLength);
    }
    function prepSig(msgHash, privateKey, opts = defaultSigOpts) {
      if (["recovered", "canonical"].some((k) => k in opts))
        throw new Error("sign() legacy options not supported");
      const { hash: hash2, randomBytes: randomBytes2 } = CURVE2;
      let { lowS, prehash, extraEntropy: ent } = opts;
      if (lowS == null)
        lowS = true;
      msgHash = ensureBytes("msgHash", msgHash);
      if (prehash)
        msgHash = ensureBytes("prehashed msgHash", hash2(msgHash));
      const h1int = bits2int_modN(msgHash);
      const d = normPrivateKeyToScalar(privateKey);
      const seedArgs = [int2octets(d), int2octets(h1int)];
      if (ent != null && ent !== false) {
        const e = ent === true ? randomBytes2(Fp8.BYTES) : ent;
        seedArgs.push(ensureBytes("extraEntropy", e));
      }
      const seed = concatBytes(...seedArgs);
      const m = h1int;
      function k2sig(kBytes) {
        const k = bits2int(kBytes);
        if (!isWithinCurveOrder(k))
          return;
        const ik = invN(k);
        const q = Point2.BASE.multiply(k).toAffine();
        const r = modN2(q.x);
        if (r === _0n4)
          return;
        const s = modN2(ik * modN2(m + r * d));
        if (s === _0n4)
          return;
        let recovery = (q.x === r ? 0 : 2) | Number(q.y & _1n4);
        let normS = s;
        if (lowS && isBiggerThanHalfOrder(s)) {
          normS = normalizeS(s);
          recovery ^= 1;
        }
        return new Signature(r, normS, recovery);
      }
      return { seed, k2sig };
    }
    const defaultSigOpts = { lowS: CURVE2.lowS, prehash: false };
    const defaultVerOpts = { lowS: CURVE2.lowS, prehash: false };
    function sign(msgHash, privKey, opts = defaultSigOpts) {
      const { seed, k2sig } = prepSig(msgHash, privKey, opts);
      const C = CURVE2;
      const drbg = createHmacDrbg(C.hash.outputLen, C.nByteLength, C.hmac);
      return drbg(seed, k2sig);
    }
    Point2.BASE._setWindowSize(8);
    function verify(signature, msgHash, publicKey, opts = defaultVerOpts) {
      const sg = signature;
      msgHash = ensureBytes("msgHash", msgHash);
      publicKey = ensureBytes("publicKey", publicKey);
      if ("strict" in opts)
        throw new Error("options.strict was renamed to lowS");
      const { lowS, prehash } = opts;
      let _sig = void 0;
      let P3;
      try {
        if (typeof sg === "string" || isBytes(sg)) {
          try {
            _sig = Signature.fromDER(sg);
          } catch (derError) {
            if (!(derError instanceof DER.Err))
              throw derError;
            _sig = Signature.fromCompact(sg);
          }
        } else if (typeof sg === "object" && typeof sg.r === "bigint" && typeof sg.s === "bigint") {
          const { r: r2, s: s2 } = sg;
          _sig = new Signature(r2, s2);
        } else {
          throw new Error("PARSE");
        }
        P3 = Point2.fromHex(publicKey);
      } catch (error) {
        if (error.message === "PARSE")
          throw new Error(`signature must be Signature instance, Uint8Array or hex string`);
        return false;
      }
      if (lowS && _sig.hasHighS())
        return false;
      if (prehash)
        msgHash = CURVE2.hash(msgHash);
      const { r, s } = _sig;
      const h = bits2int_modN(msgHash);
      const is = invN(s);
      const u1 = modN2(h * is);
      const u2 = modN2(r * is);
      const R = Point2.BASE.multiplyAndAddUnsafe(P3, u1, u2)?.toAffine();
      if (!R)
        return false;
      const v = modN2(R.x);
      return v === r;
    }
    return {
      CURVE: CURVE2,
      getPublicKey,
      getSharedSecret,
      sign,
      verify,
      ProjectivePoint: Point2,
      Signature,
      utils: utils2
    };
  }
  function SWUFpSqrtRatio(Fp8, Z) {
    const q = Fp8.ORDER;
    let l = _0n4;
    for (let o = q - _1n4; o % _2n3 === _0n4; o /= _2n3)
      l += _1n4;
    const c1 = l;
    const _2n_pow_c1_1 = _2n3 << c1 - _1n4 - _1n4;
    const _2n_pow_c1 = _2n_pow_c1_1 * _2n3;
    const c2 = (q - _1n4) / _2n_pow_c1;
    const c3 = (c2 - _1n4) / _2n3;
    const c4 = _2n_pow_c1 - _1n4;
    const c5 = _2n_pow_c1_1;
    const c6 = Fp8.pow(Z, c2);
    const c7 = Fp8.pow(Z, (c2 + _1n4) / _2n3);
    let sqrtRatio = (u, v) => {
      let tv1 = c6;
      let tv2 = Fp8.pow(v, c4);
      let tv3 = Fp8.sqr(tv2);
      tv3 = Fp8.mul(tv3, v);
      let tv5 = Fp8.mul(u, tv3);
      tv5 = Fp8.pow(tv5, c3);
      tv5 = Fp8.mul(tv5, tv2);
      tv2 = Fp8.mul(tv5, v);
      tv3 = Fp8.mul(tv5, u);
      let tv4 = Fp8.mul(tv3, tv2);
      tv5 = Fp8.pow(tv4, c5);
      let isQR = Fp8.eql(tv5, Fp8.ONE);
      tv2 = Fp8.mul(tv3, c7);
      tv5 = Fp8.mul(tv4, tv1);
      tv3 = Fp8.cmov(tv2, tv3, isQR);
      tv4 = Fp8.cmov(tv5, tv4, isQR);
      for (let i = c1; i > _1n4; i--) {
        let tv52 = i - _2n3;
        tv52 = _2n3 << tv52 - _1n4;
        let tvv5 = Fp8.pow(tv4, tv52);
        const e1 = Fp8.eql(tvv5, Fp8.ONE);
        tv2 = Fp8.mul(tv3, tv1);
        tv1 = Fp8.mul(tv1, tv1);
        tvv5 = Fp8.mul(tv4, tv1);
        tv3 = Fp8.cmov(tv2, tv3, e1);
        tv4 = Fp8.cmov(tvv5, tv4, e1);
      }
      return { isValid: isQR, value: tv3 };
    };
    if (Fp8.ORDER % _4n2 === _3n2) {
      const c12 = (Fp8.ORDER - _3n2) / _4n2;
      const c22 = Fp8.sqrt(Fp8.neg(Z));
      sqrtRatio = (u, v) => {
        let tv1 = Fp8.sqr(v);
        const tv2 = Fp8.mul(u, v);
        tv1 = Fp8.mul(tv1, tv2);
        let y1 = Fp8.pow(tv1, c12);
        y1 = Fp8.mul(y1, tv2);
        const y2 = Fp8.mul(y1, c22);
        const tv3 = Fp8.mul(Fp8.sqr(y1), v);
        const isQR = Fp8.eql(tv3, u);
        let y = Fp8.cmov(y2, y1, isQR);
        return { isValid: isQR, value: y };
      };
    }
    return sqrtRatio;
  }
  function mapToCurveSimpleSWU(Fp8, opts) {
    validateField(Fp8);
    if (!Fp8.isValid(opts.A) || !Fp8.isValid(opts.B) || !Fp8.isValid(opts.Z))
      throw new Error("mapToCurveSimpleSWU: invalid opts");
    const sqrtRatio = SWUFpSqrtRatio(Fp8, opts.Z);
    if (!Fp8.isOdd)
      throw new Error("Fp.isOdd is not implemented!");
    return (u) => {
      let tv1, tv2, tv3, tv4, tv5, tv6, x, y;
      tv1 = Fp8.sqr(u);
      tv1 = Fp8.mul(tv1, opts.Z);
      tv2 = Fp8.sqr(tv1);
      tv2 = Fp8.add(tv2, tv1);
      tv3 = Fp8.add(tv2, Fp8.ONE);
      tv3 = Fp8.mul(tv3, opts.B);
      tv4 = Fp8.cmov(opts.Z, Fp8.neg(tv2), !Fp8.eql(tv2, Fp8.ZERO));
      tv4 = Fp8.mul(tv4, opts.A);
      tv2 = Fp8.sqr(tv3);
      tv6 = Fp8.sqr(tv4);
      tv5 = Fp8.mul(tv6, opts.A);
      tv2 = Fp8.add(tv2, tv5);
      tv2 = Fp8.mul(tv2, tv3);
      tv6 = Fp8.mul(tv6, tv4);
      tv5 = Fp8.mul(tv6, opts.B);
      tv2 = Fp8.add(tv2, tv5);
      x = Fp8.mul(tv1, tv3);
      const { isValid, value } = sqrtRatio(tv2, tv6);
      y = Fp8.mul(tv1, u);
      y = Fp8.mul(y, value);
      x = Fp8.cmov(x, tv3, isValid);
      y = Fp8.cmov(y, value, isValid);
      const e1 = Fp8.isOdd(u) === Fp8.isOdd(y);
      y = Fp8.cmov(Fp8.neg(y), y, e1);
      x = Fp8.div(x, tv4);
      return { x, y };
    };
  }

  // ../esm/abstract/hash-to-curve.js
  var os2ip = bytesToNumberBE;
  function i2osp(value, length) {
    if (value < 0 || value >= 1 << 8 * length) {
      throw new Error(`bad I2OSP call: value=${value} length=${length}`);
    }
    const res = Array.from({ length }).fill(0);
    for (let i = length - 1; i >= 0; i--) {
      res[i] = value & 255;
      value >>>= 8;
    }
    return new Uint8Array(res);
  }
  function strxor(a, b) {
    const arr = new Uint8Array(a.length);
    for (let i = 0; i < a.length; i++) {
      arr[i] = a[i] ^ b[i];
    }
    return arr;
  }
  function anum(item) {
    if (!Number.isSafeInteger(item))
      throw new Error("number expected");
  }
  function expand_message_xmd(msg, DST, lenInBytes, H) {
    abytes(msg);
    abytes(DST);
    anum(lenInBytes);
    if (DST.length > 255)
      DST = H(concatBytes(utf8ToBytes("H2C-OVERSIZE-DST-"), DST));
    const { outputLen: b_in_bytes, blockLen: r_in_bytes } = H;
    const ell = Math.ceil(lenInBytes / b_in_bytes);
    if (ell > 255)
      throw new Error("Invalid xmd length");
    const DST_prime = concatBytes(DST, i2osp(DST.length, 1));
    const Z_pad = i2osp(0, r_in_bytes);
    const l_i_b_str = i2osp(lenInBytes, 2);
    const b = new Array(ell);
    const b_0 = H(concatBytes(Z_pad, msg, l_i_b_str, i2osp(0, 1), DST_prime));
    b[0] = H(concatBytes(b_0, i2osp(1, 1), DST_prime));
    for (let i = 1; i <= ell; i++) {
      const args = [strxor(b_0, b[i - 1]), i2osp(i + 1, 1), DST_prime];
      b[i] = H(concatBytes(...args));
    }
    const pseudo_random_bytes = concatBytes(...b);
    return pseudo_random_bytes.slice(0, lenInBytes);
  }
  function expand_message_xof(msg, DST, lenInBytes, k, H) {
    abytes(msg);
    abytes(DST);
    anum(lenInBytes);
    if (DST.length > 255) {
      const dkLen = Math.ceil(2 * k / 8);
      DST = H.create({ dkLen }).update(utf8ToBytes("H2C-OVERSIZE-DST-")).update(DST).digest();
    }
    if (lenInBytes > 65535 || DST.length > 255)
      throw new Error("expand_message_xof: invalid lenInBytes");
    return H.create({ dkLen: lenInBytes }).update(msg).update(i2osp(lenInBytes, 2)).update(DST).update(i2osp(DST.length, 1)).digest();
  }
  function hash_to_field(msg, count, options) {
    validateObject(options, {
      DST: "stringOrUint8Array",
      p: "bigint",
      m: "isSafeInteger",
      k: "isSafeInteger",
      hash: "hash"
    });
    const { p, k, m, hash: hash2, expand, DST: _DST } = options;
    abytes(msg);
    anum(count);
    const DST = typeof _DST === "string" ? utf8ToBytes(_DST) : _DST;
    const log2p = p.toString(2).length;
    const L = Math.ceil((log2p + k) / 8);
    const len_in_bytes = count * m * L;
    let prb;
    if (expand === "xmd") {
      prb = expand_message_xmd(msg, DST, len_in_bytes, hash2);
    } else if (expand === "xof") {
      prb = expand_message_xof(msg, DST, len_in_bytes, k, hash2);
    } else if (expand === "_internal_pass") {
      prb = msg;
    } else {
      throw new Error('expand must be "xmd" or "xof"');
    }
    const u = new Array(count);
    for (let i = 0; i < count; i++) {
      const e = new Array(m);
      for (let j = 0; j < m; j++) {
        const elm_offset = L * (j + i * m);
        const tv = prb.subarray(elm_offset, elm_offset + L);
        e[j] = mod(os2ip(tv), p);
      }
      u[i] = e;
    }
    return u;
  }
  function isogenyMap(field, map) {
    const COEFF = map.map((i) => Array.from(i).reverse());
    return (x, y) => {
      const [xNum, xDen, yNum, yDen] = COEFF.map((val) => val.reduce((acc, i) => field.add(field.mul(acc, x), i)));
      x = field.div(xNum, xDen);
      y = field.mul(y, field.div(yNum, yDen));
      return { x, y };
    };
  }
  function createHasher(Point2, mapToCurve, def) {
    if (typeof mapToCurve !== "function")
      throw new Error("mapToCurve() must be defined");
    return {
      // Encodes byte string to elliptic curve.
      // hash_to_curve from https://www.rfc-editor.org/rfc/rfc9380#section-3
      hashToCurve(msg, options) {
        const u = hash_to_field(msg, 2, { ...def, DST: def.DST, ...options });
        const u0 = Point2.fromAffine(mapToCurve(u[0]));
        const u1 = Point2.fromAffine(mapToCurve(u[1]));
        const P3 = u0.add(u1).clearCofactor();
        P3.assertValidity();
        return P3;
      },
      // Encodes byte string to elliptic curve.
      // encode_to_curve from https://www.rfc-editor.org/rfc/rfc9380#section-3
      encodeToCurve(msg, options) {
        const u = hash_to_field(msg, 1, { ...def, DST: def.encodeDST, ...options });
        const P3 = Point2.fromAffine(mapToCurve(u[0])).clearCofactor();
        P3.assertValidity();
        return P3;
      }
    };
  }

  // ../node_modules/@noble/hashes/esm/hmac.js
  var HMAC = class extends Hash {
    constructor(hash2, _key) {
      super();
      this.finished = false;
      this.destroyed = false;
      hash(hash2);
      const key = toBytes(_key);
      this.iHash = hash2.create();
      if (typeof this.iHash.update !== "function")
        throw new Error("Expected instance of class which extends utils.Hash");
      this.blockLen = this.iHash.blockLen;
      this.outputLen = this.iHash.outputLen;
      const blockLen = this.blockLen;
      const pad = new Uint8Array(blockLen);
      pad.set(key.length > blockLen ? hash2.create().update(key).digest() : key);
      for (let i = 0; i < pad.length; i++)
        pad[i] ^= 54;
      this.iHash.update(pad);
      this.oHash = hash2.create();
      for (let i = 0; i < pad.length; i++)
        pad[i] ^= 54 ^ 92;
      this.oHash.update(pad);
      pad.fill(0);
    }
    update(buf) {
      exists(this);
      this.iHash.update(buf);
      return this;
    }
    digestInto(out) {
      exists(this);
      bytes(out, this.outputLen);
      this.finished = true;
      this.iHash.digestInto(out);
      this.oHash.update(out);
      this.oHash.digestInto(out);
      this.destroy();
    }
    digest() {
      const out = new Uint8Array(this.oHash.outputLen);
      this.digestInto(out);
      return out;
    }
    _cloneInto(to) {
      to || (to = Object.create(Object.getPrototypeOf(this), {}));
      const { oHash, iHash, finished, destroyed, blockLen, outputLen } = this;
      to = to;
      to.finished = finished;
      to.destroyed = destroyed;
      to.blockLen = blockLen;
      to.outputLen = outputLen;
      to.oHash = oHash._cloneInto(to.oHash);
      to.iHash = iHash._cloneInto(to.iHash);
      return to;
    }
    destroy() {
      this.destroyed = true;
      this.oHash.destroy();
      this.iHash.destroy();
    }
  };
  var hmac = (hash2, key, message) => new HMAC(hash2, key).update(message).digest();
  hmac.create = (hash2, key) => new HMAC(hash2, key);

  // ../esm/_shortw_utils.js
  function getHash(hash2) {
    return {
      hash: hash2,
      hmac: (key, ...msgs) => hmac(hash2, key, concatBytes2(...msgs)),
      randomBytes
    };
  }
  function createCurve(curveDef, defHash) {
    const create = (hash2) => weierstrass({ ...curveDef, ...getHash(hash2) });
    return Object.freeze({ ...create(defHash), create });
  }

  // ../esm/secp256k1.js
  var secp256k1P = BigInt("0xfffffffffffffffffffffffffffffffffffffffffffffffffffffffefffffc2f");
  var secp256k1N = BigInt("0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141");
  var _1n5 = BigInt(1);
  var _2n4 = BigInt(2);
  var divNearest = (a, b) => (a + b / _2n4) / b;
  function sqrtMod(y) {
    const P3 = secp256k1P;
    const _3n6 = BigInt(3), _6n = BigInt(6), _11n2 = BigInt(11), _22n2 = BigInt(22);
    const _23n = BigInt(23), _44n2 = BigInt(44), _88n2 = BigInt(88);
    const b2 = y * y * y % P3;
    const b3 = b2 * b2 * y % P3;
    const b6 = pow2(b3, _3n6, P3) * b3 % P3;
    const b9 = pow2(b6, _3n6, P3) * b3 % P3;
    const b11 = pow2(b9, _2n4, P3) * b2 % P3;
    const b22 = pow2(b11, _11n2, P3) * b11 % P3;
    const b44 = pow2(b22, _22n2, P3) * b22 % P3;
    const b88 = pow2(b44, _44n2, P3) * b44 % P3;
    const b176 = pow2(b88, _88n2, P3) * b88 % P3;
    const b220 = pow2(b176, _44n2, P3) * b44 % P3;
    const b223 = pow2(b220, _3n6, P3) * b3 % P3;
    const t1 = pow2(b223, _23n, P3) * b22 % P3;
    const t2 = pow2(t1, _6n, P3) * b2 % P3;
    const root = pow2(t2, _2n4, P3);
    if (!Fp.eql(Fp.sqr(root), y))
      throw new Error("Cannot find square root");
    return root;
  }
  var Fp = Field(secp256k1P, void 0, void 0, { sqrt: sqrtMod });
  var secp256k1 = createCurve({
    a: BigInt(0),
    // equation params: a, b
    b: BigInt(7),
    // Seem to be rigid: bitcointalk.org/index.php?topic=289795.msg3183975#msg3183975
    Fp,
    // Field's prime: 2n**256n - 2n**32n - 2n**9n - 2n**8n - 2n**7n - 2n**6n - 2n**4n - 1n
    n: secp256k1N,
    // Curve order, total count of valid points in the field
    // Base point (x, y) aka generator point
    Gx: BigInt("55066263022277343669578718895168534326250603453777594175500187360389116729240"),
    Gy: BigInt("32670510020758816978083085130507043184471273380659243275938904335757337482424"),
    h: BigInt(1),
    // Cofactor
    lowS: true,
    // Allow only low-S signatures by default in sign() and verify()
    /**
     * secp256k1 belongs to Koblitz curves: it has efficiently computable endomorphism.
     * Endomorphism uses 2x less RAM, speeds up precomputation by 2x and ECDH / key recovery by 20%.
     * For precomputed wNAF it trades off 1/2 init time & 1/3 ram for 20% perf hit.
     * Explanation: https://gist.github.com/paulmillr/eb670806793e84df628a7c434a873066
     */
    endo: {
      beta: BigInt("0x7ae96a2b657c07106e64479eac3434e99cf0497512f58995c1396c28719501ee"),
      splitScalar: (k) => {
        const n = secp256k1N;
        const a1 = BigInt("0x3086d221a7d46bcde86c90e49284eb15");
        const b1 = -_1n5 * BigInt("0xe4437ed6010e88286f547fa90abfe4c3");
        const a2 = BigInt("0x114ca50f7a8e2f3f657c1108d9d44cfd8");
        const b2 = a1;
        const POW_2_128 = BigInt("0x100000000000000000000000000000000");
        const c1 = divNearest(b2 * k, n);
        const c2 = divNearest(-b1 * k, n);
        let k1 = mod(k - c1 * a1 - c2 * a2, n);
        let k2 = mod(-c1 * b1 - c2 * b2, n);
        const k1neg = k1 > POW_2_128;
        const k2neg = k2 > POW_2_128;
        if (k1neg)
          k1 = n - k1;
        if (k2neg)
          k2 = n - k2;
        if (k1 > POW_2_128 || k2 > POW_2_128) {
          throw new Error("splitScalar: Endomorphism failed, k=" + k);
        }
        return { k1neg, k1, k2neg, k2 };
      }
    }
  }, sha256);
  var _0n5 = BigInt(0);
  var fe = (x) => typeof x === "bigint" && _0n5 < x && x < secp256k1P;
  var ge = (x) => typeof x === "bigint" && _0n5 < x && x < secp256k1N;
  var TAGGED_HASH_PREFIXES = {};
  function taggedHash(tag, ...messages) {
    let tagP = TAGGED_HASH_PREFIXES[tag];
    if (tagP === void 0) {
      const tagH = sha256(Uint8Array.from(tag, (c) => c.charCodeAt(0)));
      tagP = concatBytes(tagH, tagH);
      TAGGED_HASH_PREFIXES[tag] = tagP;
    }
    return sha256(concatBytes(tagP, ...messages));
  }
  var pointToBytes = (point) => point.toRawBytes(true).slice(1);
  var numTo32b = (n) => numberToBytesBE(n, 32);
  var modP = (x) => mod(x, secp256k1P);
  var modN = (x) => mod(x, secp256k1N);
  var Point = secp256k1.ProjectivePoint;
  var GmulAdd = (Q, a, b) => Point.BASE.multiplyAndAddUnsafe(Q, a, b);
  function schnorrGetExtPubKey(priv) {
    let d_ = secp256k1.utils.normPrivateKeyToScalar(priv);
    let p = Point.fromPrivateKey(d_);
    const scalar = p.hasEvenY() ? d_ : modN(-d_);
    return { scalar, bytes: pointToBytes(p) };
  }
  function lift_x(x) {
    if (!fe(x))
      throw new Error("bad x: need 0 < x < p");
    const xx = modP(x * x);
    const c = modP(xx * x + BigInt(7));
    let y = sqrtMod(c);
    if (y % _2n4 !== _0n5)
      y = modP(-y);
    const p = new Point(x, y, _1n5);
    p.assertValidity();
    return p;
  }
  function challenge(...args) {
    return modN(bytesToNumberBE(taggedHash("BIP0340/challenge", ...args)));
  }
  function schnorrGetPublicKey(privateKey) {
    return schnorrGetExtPubKey(privateKey).bytes;
  }
  function schnorrSign(message, privateKey, auxRand = randomBytes(32)) {
    const m = ensureBytes("message", message);
    const { bytes: px, scalar: d } = schnorrGetExtPubKey(privateKey);
    const a = ensureBytes("auxRand", auxRand, 32);
    const t = numTo32b(d ^ bytesToNumberBE(taggedHash("BIP0340/aux", a)));
    const rand = taggedHash("BIP0340/nonce", t, px, m);
    const k_ = modN(bytesToNumberBE(rand));
    if (k_ === _0n5)
      throw new Error("sign failed: k is zero");
    const { bytes: rx, scalar: k } = schnorrGetExtPubKey(k_);
    const e = challenge(rx, px, m);
    const sig = new Uint8Array(64);
    sig.set(rx, 0);
    sig.set(numTo32b(modN(k + e * d)), 32);
    if (!schnorrVerify(sig, m, px))
      throw new Error("sign: Invalid signature produced");
    return sig;
  }
  function schnorrVerify(signature, message, publicKey) {
    const sig = ensureBytes("signature", signature, 64);
    const m = ensureBytes("message", message);
    const pub = ensureBytes("publicKey", publicKey, 32);
    try {
      const P3 = lift_x(bytesToNumberBE(pub));
      const r = bytesToNumberBE(sig.subarray(0, 32));
      if (!fe(r))
        return false;
      const s = bytesToNumberBE(sig.subarray(32, 64));
      if (!ge(s))
        return false;
      const e = challenge(numTo32b(r), pointToBytes(P3), m);
      const R = GmulAdd(P3, s, modN(-e));
      if (!R || !R.hasEvenY() || R.toAffine().x !== r)
        return false;
      return true;
    } catch (error) {
      return false;
    }
  }
  var schnorr = /* @__PURE__ */ (() => ({
    getPublicKey: schnorrGetPublicKey,
    sign: schnorrSign,
    verify: schnorrVerify,
    utils: {
      randomPrivateKey: secp256k1.utils.randomPrivateKey,
      lift_x,
      pointToBytes,
      numberToBytesBE,
      bytesToNumberBE,
      taggedHash,
      mod
    }
  }))();

  // ../node_modules/@noble/hashes/esm/_u64.js
  var U32_MASK64 = /* @__PURE__ */ BigInt(2 ** 32 - 1);
  var _32n = /* @__PURE__ */ BigInt(32);
  function fromBig(n, le = false) {
    if (le)
      return { h: Number(n & U32_MASK64), l: Number(n >> _32n & U32_MASK64) };
    return { h: Number(n >> _32n & U32_MASK64) | 0, l: Number(n & U32_MASK64) | 0 };
  }
  function split(lst, le = false) {
    let Ah = new Uint32Array(lst.length);
    let Al = new Uint32Array(lst.length);
    for (let i = 0; i < lst.length; i++) {
      const { h, l } = fromBig(lst[i], le);
      [Ah[i], Al[i]] = [h, l];
    }
    return [Ah, Al];
  }
  var toBig = (h, l) => BigInt(h >>> 0) << _32n | BigInt(l >>> 0);
  var shrSH = (h, _l, s) => h >>> s;
  var shrSL = (h, l, s) => h << 32 - s | l >>> s;
  var rotrSH = (h, l, s) => h >>> s | l << 32 - s;
  var rotrSL = (h, l, s) => h << 32 - s | l >>> s;
  var rotrBH = (h, l, s) => h << 64 - s | l >>> s - 32;
  var rotrBL = (h, l, s) => h >>> s - 32 | l << 64 - s;
  var rotr32H = (_h, l) => l;
  var rotr32L = (h, _l) => h;
  var rotlSH = (h, l, s) => h << s | l >>> 32 - s;
  var rotlSL = (h, l, s) => l << s | h >>> 32 - s;
  var rotlBH = (h, l, s) => l << s - 32 | h >>> 64 - s;
  var rotlBL = (h, l, s) => h << s - 32 | l >>> 64 - s;
  function add(Ah, Al, Bh, Bl) {
    const l = (Al >>> 0) + (Bl >>> 0);
    return { h: Ah + Bh + (l / 2 ** 32 | 0) | 0, l: l | 0 };
  }
  var add3L = (Al, Bl, Cl) => (Al >>> 0) + (Bl >>> 0) + (Cl >>> 0);
  var add3H = (low, Ah, Bh, Ch) => Ah + Bh + Ch + (low / 2 ** 32 | 0) | 0;
  var add4L = (Al, Bl, Cl, Dl) => (Al >>> 0) + (Bl >>> 0) + (Cl >>> 0) + (Dl >>> 0);
  var add4H = (low, Ah, Bh, Ch, Dh) => Ah + Bh + Ch + Dh + (low / 2 ** 32 | 0) | 0;
  var add5L = (Al, Bl, Cl, Dl, El) => (Al >>> 0) + (Bl >>> 0) + (Cl >>> 0) + (Dl >>> 0) + (El >>> 0);
  var add5H = (low, Ah, Bh, Ch, Dh, Eh) => Ah + Bh + Ch + Dh + Eh + (low / 2 ** 32 | 0) | 0;
  var u64 = {
    fromBig,
    split,
    toBig,
    shrSH,
    shrSL,
    rotrSH,
    rotrSL,
    rotrBH,
    rotrBL,
    rotr32H,
    rotr32L,
    rotlSH,
    rotlSL,
    rotlBH,
    rotlBL,
    add,
    add3L,
    add3H,
    add4L,
    add4H,
    add5H,
    add5L
  };
  var u64_default = u64;

  // ../node_modules/@noble/hashes/esm/sha512.js
  var [SHA512_Kh, SHA512_Kl] = /* @__PURE__ */ (() => u64_default.split([
    "0x428a2f98d728ae22",
    "0x7137449123ef65cd",
    "0xb5c0fbcfec4d3b2f",
    "0xe9b5dba58189dbbc",
    "0x3956c25bf348b538",
    "0x59f111f1b605d019",
    "0x923f82a4af194f9b",
    "0xab1c5ed5da6d8118",
    "0xd807aa98a3030242",
    "0x12835b0145706fbe",
    "0x243185be4ee4b28c",
    "0x550c7dc3d5ffb4e2",
    "0x72be5d74f27b896f",
    "0x80deb1fe3b1696b1",
    "0x9bdc06a725c71235",
    "0xc19bf174cf692694",
    "0xe49b69c19ef14ad2",
    "0xefbe4786384f25e3",
    "0x0fc19dc68b8cd5b5",
    "0x240ca1cc77ac9c65",
    "0x2de92c6f592b0275",
    "0x4a7484aa6ea6e483",
    "0x5cb0a9dcbd41fbd4",
    "0x76f988da831153b5",
    "0x983e5152ee66dfab",
    "0xa831c66d2db43210",
    "0xb00327c898fb213f",
    "0xbf597fc7beef0ee4",
    "0xc6e00bf33da88fc2",
    "0xd5a79147930aa725",
    "0x06ca6351e003826f",
    "0x142929670a0e6e70",
    "0x27b70a8546d22ffc",
    "0x2e1b21385c26c926",
    "0x4d2c6dfc5ac42aed",
    "0x53380d139d95b3df",
    "0x650a73548baf63de",
    "0x766a0abb3c77b2a8",
    "0x81c2c92e47edaee6",
    "0x92722c851482353b",
    "0xa2bfe8a14cf10364",
    "0xa81a664bbc423001",
    "0xc24b8b70d0f89791",
    "0xc76c51a30654be30",
    "0xd192e819d6ef5218",
    "0xd69906245565a910",
    "0xf40e35855771202a",
    "0x106aa07032bbd1b8",
    "0x19a4c116b8d2d0c8",
    "0x1e376c085141ab53",
    "0x2748774cdf8eeb99",
    "0x34b0bcb5e19b48a8",
    "0x391c0cb3c5c95a63",
    "0x4ed8aa4ae3418acb",
    "0x5b9cca4f7763e373",
    "0x682e6ff3d6b2b8a3",
    "0x748f82ee5defb2fc",
    "0x78a5636f43172f60",
    "0x84c87814a1f0ab72",
    "0x8cc702081a6439ec",
    "0x90befffa23631e28",
    "0xa4506cebde82bde9",
    "0xbef9a3f7b2c67915",
    "0xc67178f2e372532b",
    "0xca273eceea26619c",
    "0xd186b8c721c0c207",
    "0xeada7dd6cde0eb1e",
    "0xf57d4f7fee6ed178",
    "0x06f067aa72176fba",
    "0x0a637dc5a2c898a6",
    "0x113f9804bef90dae",
    "0x1b710b35131c471b",
    "0x28db77f523047d84",
    "0x32caab7b40c72493",
    "0x3c9ebe0a15c9bebc",
    "0x431d67c49c100d4c",
    "0x4cc5d4becb3e42b6",
    "0x597f299cfc657e2a",
    "0x5fcb6fab3ad6faec",
    "0x6c44198c4a475817"
  ].map((n) => BigInt(n))))();
  var SHA512_W_H = /* @__PURE__ */ new Uint32Array(80);
  var SHA512_W_L = /* @__PURE__ */ new Uint32Array(80);
  var SHA512 = class extends HashMD {
    constructor() {
      super(128, 64, 16, false);
      this.Ah = 1779033703 | 0;
      this.Al = 4089235720 | 0;
      this.Bh = 3144134277 | 0;
      this.Bl = 2227873595 | 0;
      this.Ch = 1013904242 | 0;
      this.Cl = 4271175723 | 0;
      this.Dh = 2773480762 | 0;
      this.Dl = 1595750129 | 0;
      this.Eh = 1359893119 | 0;
      this.El = 2917565137 | 0;
      this.Fh = 2600822924 | 0;
      this.Fl = 725511199 | 0;
      this.Gh = 528734635 | 0;
      this.Gl = 4215389547 | 0;
      this.Hh = 1541459225 | 0;
      this.Hl = 327033209 | 0;
    }
    // prettier-ignore
    get() {
      const { Ah, Al, Bh, Bl, Ch, Cl, Dh, Dl, Eh, El, Fh, Fl, Gh, Gl, Hh, Hl } = this;
      return [Ah, Al, Bh, Bl, Ch, Cl, Dh, Dl, Eh, El, Fh, Fl, Gh, Gl, Hh, Hl];
    }
    // prettier-ignore
    set(Ah, Al, Bh, Bl, Ch, Cl, Dh, Dl, Eh, El, Fh, Fl, Gh, Gl, Hh, Hl) {
      this.Ah = Ah | 0;
      this.Al = Al | 0;
      this.Bh = Bh | 0;
      this.Bl = Bl | 0;
      this.Ch = Ch | 0;
      this.Cl = Cl | 0;
      this.Dh = Dh | 0;
      this.Dl = Dl | 0;
      this.Eh = Eh | 0;
      this.El = El | 0;
      this.Fh = Fh | 0;
      this.Fl = Fl | 0;
      this.Gh = Gh | 0;
      this.Gl = Gl | 0;
      this.Hh = Hh | 0;
      this.Hl = Hl | 0;
    }
    process(view, offset) {
      for (let i = 0; i < 16; i++, offset += 4) {
        SHA512_W_H[i] = view.getUint32(offset);
        SHA512_W_L[i] = view.getUint32(offset += 4);
      }
      for (let i = 16; i < 80; i++) {
        const W15h = SHA512_W_H[i - 15] | 0;
        const W15l = SHA512_W_L[i - 15] | 0;
        const s0h = u64_default.rotrSH(W15h, W15l, 1) ^ u64_default.rotrSH(W15h, W15l, 8) ^ u64_default.shrSH(W15h, W15l, 7);
        const s0l = u64_default.rotrSL(W15h, W15l, 1) ^ u64_default.rotrSL(W15h, W15l, 8) ^ u64_default.shrSL(W15h, W15l, 7);
        const W2h = SHA512_W_H[i - 2] | 0;
        const W2l = SHA512_W_L[i - 2] | 0;
        const s1h = u64_default.rotrSH(W2h, W2l, 19) ^ u64_default.rotrBH(W2h, W2l, 61) ^ u64_default.shrSH(W2h, W2l, 6);
        const s1l = u64_default.rotrSL(W2h, W2l, 19) ^ u64_default.rotrBL(W2h, W2l, 61) ^ u64_default.shrSL(W2h, W2l, 6);
        const SUMl = u64_default.add4L(s0l, s1l, SHA512_W_L[i - 7], SHA512_W_L[i - 16]);
        const SUMh = u64_default.add4H(SUMl, s0h, s1h, SHA512_W_H[i - 7], SHA512_W_H[i - 16]);
        SHA512_W_H[i] = SUMh | 0;
        SHA512_W_L[i] = SUMl | 0;
      }
      let { Ah, Al, Bh, Bl, Ch, Cl, Dh, Dl, Eh, El, Fh, Fl, Gh, Gl, Hh, Hl } = this;
      for (let i = 0; i < 80; i++) {
        const sigma1h = u64_default.rotrSH(Eh, El, 14) ^ u64_default.rotrSH(Eh, El, 18) ^ u64_default.rotrBH(Eh, El, 41);
        const sigma1l = u64_default.rotrSL(Eh, El, 14) ^ u64_default.rotrSL(Eh, El, 18) ^ u64_default.rotrBL(Eh, El, 41);
        const CHIh = Eh & Fh ^ ~Eh & Gh;
        const CHIl = El & Fl ^ ~El & Gl;
        const T1ll = u64_default.add5L(Hl, sigma1l, CHIl, SHA512_Kl[i], SHA512_W_L[i]);
        const T1h = u64_default.add5H(T1ll, Hh, sigma1h, CHIh, SHA512_Kh[i], SHA512_W_H[i]);
        const T1l = T1ll | 0;
        const sigma0h = u64_default.rotrSH(Ah, Al, 28) ^ u64_default.rotrBH(Ah, Al, 34) ^ u64_default.rotrBH(Ah, Al, 39);
        const sigma0l = u64_default.rotrSL(Ah, Al, 28) ^ u64_default.rotrBL(Ah, Al, 34) ^ u64_default.rotrBL(Ah, Al, 39);
        const MAJh = Ah & Bh ^ Ah & Ch ^ Bh & Ch;
        const MAJl = Al & Bl ^ Al & Cl ^ Bl & Cl;
        Hh = Gh | 0;
        Hl = Gl | 0;
        Gh = Fh | 0;
        Gl = Fl | 0;
        Fh = Eh | 0;
        Fl = El | 0;
        ({ h: Eh, l: El } = u64_default.add(Dh | 0, Dl | 0, T1h | 0, T1l | 0));
        Dh = Ch | 0;
        Dl = Cl | 0;
        Ch = Bh | 0;
        Cl = Bl | 0;
        Bh = Ah | 0;
        Bl = Al | 0;
        const All = u64_default.add3L(T1l, sigma0l, MAJl);
        Ah = u64_default.add3H(All, T1h, sigma0h, MAJh);
        Al = All | 0;
      }
      ({ h: Ah, l: Al } = u64_default.add(this.Ah | 0, this.Al | 0, Ah | 0, Al | 0));
      ({ h: Bh, l: Bl } = u64_default.add(this.Bh | 0, this.Bl | 0, Bh | 0, Bl | 0));
      ({ h: Ch, l: Cl } = u64_default.add(this.Ch | 0, this.Cl | 0, Ch | 0, Cl | 0));
      ({ h: Dh, l: Dl } = u64_default.add(this.Dh | 0, this.Dl | 0, Dh | 0, Dl | 0));
      ({ h: Eh, l: El } = u64_default.add(this.Eh | 0, this.El | 0, Eh | 0, El | 0));
      ({ h: Fh, l: Fl } = u64_default.add(this.Fh | 0, this.Fl | 0, Fh | 0, Fl | 0));
      ({ h: Gh, l: Gl } = u64_default.add(this.Gh | 0, this.Gl | 0, Gh | 0, Gl | 0));
      ({ h: Hh, l: Hl } = u64_default.add(this.Hh | 0, this.Hl | 0, Hh | 0, Hl | 0));
      this.set(Ah, Al, Bh, Bl, Ch, Cl, Dh, Dl, Eh, El, Fh, Fl, Gh, Gl, Hh, Hl);
    }
    roundClean() {
      SHA512_W_H.fill(0);
      SHA512_W_L.fill(0);
    }
    destroy() {
      this.buffer.fill(0);
      this.set(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0);
    }
  };
  var SHA384 = class extends SHA512 {
    constructor() {
      super();
      this.Ah = 3418070365 | 0;
      this.Al = 3238371032 | 0;
      this.Bh = 1654270250 | 0;
      this.Bl = 914150663 | 0;
      this.Ch = 2438529370 | 0;
      this.Cl = 812702999 | 0;
      this.Dh = 355462360 | 0;
      this.Dl = 4144912697 | 0;
      this.Eh = 1731405415 | 0;
      this.El = 4290775857 | 0;
      this.Fh = 2394180231 | 0;
      this.Fl = 1750603025 | 0;
      this.Gh = 3675008525 | 0;
      this.Gl = 1694076839 | 0;
      this.Hh = 1203062813 | 0;
      this.Hl = 3204075428 | 0;
      this.outputLen = 48;
    }
  };
  var sha512 = /* @__PURE__ */ wrapConstructor(() => new SHA512());
  var sha384 = /* @__PURE__ */ wrapConstructor(() => new SHA384());

  // ../esm/abstract/edwards.js
  var _0n6 = BigInt(0);
  var _1n6 = BigInt(1);
  var _2n5 = BigInt(2);
  var _8n2 = BigInt(8);
  var VERIFY_DEFAULT = { zip215: true };
  function validateOpts2(curve) {
    const opts = validateBasic(curve);
    validateObject(curve, {
      hash: "function",
      a: "bigint",
      d: "bigint",
      randomBytes: "function"
    }, {
      adjustScalarBytes: "function",
      domain: "function",
      uvRatio: "function",
      mapToCurve: "function"
    });
    return Object.freeze({ ...opts });
  }
  function twistedEdwards(curveDef) {
    const CURVE2 = validateOpts2(curveDef);
    const { Fp: Fp8, n: CURVE_ORDER, prehash, hash: cHash, randomBytes: randomBytes2, nByteLength, h: cofactor } = CURVE2;
    const MASK = _2n5 << BigInt(nByteLength * 8) - _1n6;
    const modP2 = Fp8.create;
    const uvRatio3 = CURVE2.uvRatio || ((u, v) => {
      try {
        return { isValid: true, value: Fp8.sqrt(u * Fp8.inv(v)) };
      } catch (e) {
        return { isValid: false, value: _0n6 };
      }
    });
    const adjustScalarBytes3 = CURVE2.adjustScalarBytes || ((bytes2) => bytes2);
    const domain = CURVE2.domain || ((data, ctx, phflag) => {
      if (ctx.length || phflag)
        throw new Error("Contexts/pre-hash are not supported");
      return data;
    });
    const inBig = (n) => typeof n === "bigint" && _0n6 < n;
    const inRange = (n, max) => inBig(n) && inBig(max) && n < max;
    const in0MaskRange = (n) => n === _0n6 || inRange(n, MASK);
    function assertInRange(n, max) {
      if (inRange(n, max))
        return n;
      throw new Error(`Expected valid scalar < ${max}, got ${typeof n} ${n}`);
    }
    function assertGE0(n) {
      return n === _0n6 ? n : assertInRange(n, CURVE_ORDER);
    }
    const pointPrecomputes = /* @__PURE__ */ new Map();
    function isPoint(other) {
      if (!(other instanceof Point2))
        throw new Error("ExtendedPoint expected");
    }
    class Point2 {
      constructor(ex, ey, ez, et) {
        this.ex = ex;
        this.ey = ey;
        this.ez = ez;
        this.et = et;
        if (!in0MaskRange(ex))
          throw new Error("x required");
        if (!in0MaskRange(ey))
          throw new Error("y required");
        if (!in0MaskRange(ez))
          throw new Error("z required");
        if (!in0MaskRange(et))
          throw new Error("t required");
      }
      get x() {
        return this.toAffine().x;
      }
      get y() {
        return this.toAffine().y;
      }
      static fromAffine(p) {
        if (p instanceof Point2)
          throw new Error("extended point not allowed");
        const { x, y } = p || {};
        if (!in0MaskRange(x) || !in0MaskRange(y))
          throw new Error("invalid affine point");
        return new Point2(x, y, _1n6, modP2(x * y));
      }
      static normalizeZ(points) {
        const toInv = Fp8.invertBatch(points.map((p) => p.ez));
        return points.map((p, i) => p.toAffine(toInv[i])).map(Point2.fromAffine);
      }
      // "Private method", don't use it directly
      _setWindowSize(windowSize) {
        this._WINDOW_SIZE = windowSize;
        pointPrecomputes.delete(this);
      }
      // Not required for fromHex(), which always creates valid points.
      // Could be useful for fromAffine().
      assertValidity() {
        const { a, d } = CURVE2;
        if (this.is0())
          throw new Error("bad point: ZERO");
        const { ex: X, ey: Y, ez: Z, et: T } = this;
        const X2 = modP2(X * X);
        const Y2 = modP2(Y * Y);
        const Z2 = modP2(Z * Z);
        const Z4 = modP2(Z2 * Z2);
        const aX2 = modP2(X2 * a);
        const left = modP2(Z2 * modP2(aX2 + Y2));
        const right = modP2(Z4 + modP2(d * modP2(X2 * Y2)));
        if (left !== right)
          throw new Error("bad point: equation left != right (1)");
        const XY = modP2(X * Y);
        const ZT = modP2(Z * T);
        if (XY !== ZT)
          throw new Error("bad point: equation left != right (2)");
      }
      // Compare one point to another.
      equals(other) {
        isPoint(other);
        const { ex: X1, ey: Y1, ez: Z1 } = this;
        const { ex: X2, ey: Y2, ez: Z2 } = other;
        const X1Z2 = modP2(X1 * Z2);
        const X2Z1 = modP2(X2 * Z1);
        const Y1Z2 = modP2(Y1 * Z2);
        const Y2Z1 = modP2(Y2 * Z1);
        return X1Z2 === X2Z1 && Y1Z2 === Y2Z1;
      }
      is0() {
        return this.equals(Point2.ZERO);
      }
      negate() {
        return new Point2(modP2(-this.ex), this.ey, this.ez, modP2(-this.et));
      }
      // Fast algo for doubling Extended Point.
      // https://hyperelliptic.org/EFD/g1p/auto-twisted-extended.html#doubling-dbl-2008-hwcd
      // Cost: 4M + 4S + 1*a + 6add + 1*2.
      double() {
        const { a } = CURVE2;
        const { ex: X1, ey: Y1, ez: Z1 } = this;
        const A = modP2(X1 * X1);
        const B = modP2(Y1 * Y1);
        const C = modP2(_2n5 * modP2(Z1 * Z1));
        const D = modP2(a * A);
        const x1y1 = X1 + Y1;
        const E = modP2(modP2(x1y1 * x1y1) - A - B);
        const G2 = D + B;
        const F = G2 - C;
        const H = D - B;
        const X3 = modP2(E * F);
        const Y3 = modP2(G2 * H);
        const T3 = modP2(E * H);
        const Z3 = modP2(F * G2);
        return new Point2(X3, Y3, Z3, T3);
      }
      // Fast algo for adding 2 Extended Points.
      // https://hyperelliptic.org/EFD/g1p/auto-twisted-extended.html#addition-add-2008-hwcd
      // Cost: 9M + 1*a + 1*d + 7add.
      add(other) {
        isPoint(other);
        const { a, d } = CURVE2;
        const { ex: X1, ey: Y1, ez: Z1, et: T1 } = this;
        const { ex: X2, ey: Y2, ez: Z2, et: T2 } = other;
        if (a === BigInt(-1)) {
          const A2 = modP2((Y1 - X1) * (Y2 + X2));
          const B2 = modP2((Y1 + X1) * (Y2 - X2));
          const F2 = modP2(B2 - A2);
          if (F2 === _0n6)
            return this.double();
          const C2 = modP2(Z1 * _2n5 * T2);
          const D2 = modP2(T1 * _2n5 * Z2);
          const E2 = D2 + C2;
          const G3 = B2 + A2;
          const H2 = D2 - C2;
          const X32 = modP2(E2 * F2);
          const Y32 = modP2(G3 * H2);
          const T32 = modP2(E2 * H2);
          const Z32 = modP2(F2 * G3);
          return new Point2(X32, Y32, Z32, T32);
        }
        const A = modP2(X1 * X2);
        const B = modP2(Y1 * Y2);
        const C = modP2(T1 * d * T2);
        const D = modP2(Z1 * Z2);
        const E = modP2((X1 + Y1) * (X2 + Y2) - A - B);
        const F = D - C;
        const G2 = D + C;
        const H = modP2(B - a * A);
        const X3 = modP2(E * F);
        const Y3 = modP2(G2 * H);
        const T3 = modP2(E * H);
        const Z3 = modP2(F * G2);
        return new Point2(X3, Y3, Z3, T3);
      }
      subtract(other) {
        return this.add(other.negate());
      }
      wNAF(n) {
        return wnaf.wNAFCached(this, pointPrecomputes, n, Point2.normalizeZ);
      }
      // Constant-time multiplication.
      multiply(scalar) {
        const { p, f } = this.wNAF(assertInRange(scalar, CURVE_ORDER));
        return Point2.normalizeZ([p, f])[0];
      }
      // Non-constant-time multiplication. Uses double-and-add algorithm.
      // It's faster, but should only be used when you don't care about
      // an exposed private key e.g. sig verification.
      // Does NOT allow scalars higher than CURVE.n.
      multiplyUnsafe(scalar) {
        let n = assertGE0(scalar);
        if (n === _0n6)
          return I;
        if (this.equals(I) || n === _1n6)
          return this;
        if (this.equals(G))
          return this.wNAF(n).p;
        return wnaf.unsafeLadder(this, n);
      }
      // Checks if point is of small order.
      // If you add something to small order point, you will have "dirty"
      // point with torsion component.
      // Multiplies point by cofactor and checks if the result is 0.
      isSmallOrder() {
        return this.multiplyUnsafe(cofactor).is0();
      }
      // Multiplies point by curve order and checks if the result is 0.
      // Returns `false` is the point is dirty.
      isTorsionFree() {
        return wnaf.unsafeLadder(this, CURVE_ORDER).is0();
      }
      // Converts Extended point to default (x, y) coordinates.
      // Can accept precomputed Z^-1 - for example, from invertBatch.
      toAffine(iz) {
        const { ex: x, ey: y, ez: z } = this;
        const is0 = this.is0();
        if (iz == null)
          iz = is0 ? _8n2 : Fp8.inv(z);
        const ax = modP2(x * iz);
        const ay = modP2(y * iz);
        const zz = modP2(z * iz);
        if (is0)
          return { x: _0n6, y: _1n6 };
        if (zz !== _1n6)
          throw new Error("invZ was invalid");
        return { x: ax, y: ay };
      }
      clearCofactor() {
        const { h: cofactor2 } = CURVE2;
        if (cofactor2 === _1n6)
          return this;
        return this.multiplyUnsafe(cofactor2);
      }
      // Converts hash string or Uint8Array to Point.
      // Uses algo from RFC8032 5.1.3.
      static fromHex(hex, zip215 = false) {
        const { d, a } = CURVE2;
        const len = Fp8.BYTES;
        hex = ensureBytes("pointHex", hex, len);
        const normed = hex.slice();
        const lastByte = hex[len - 1];
        normed[len - 1] = lastByte & ~128;
        const y = bytesToNumberLE(normed);
        if (y === _0n6) {
        } else {
          if (zip215)
            assertInRange(y, MASK);
          else
            assertInRange(y, Fp8.ORDER);
        }
        const y2 = modP2(y * y);
        const u = modP2(y2 - _1n6);
        const v = modP2(d * y2 - a);
        let { isValid, value: x } = uvRatio3(u, v);
        if (!isValid)
          throw new Error("Point.fromHex: invalid y coordinate");
        const isXOdd = (x & _1n6) === _1n6;
        const isLastByteOdd = (lastByte & 128) !== 0;
        if (!zip215 && x === _0n6 && isLastByteOdd)
          throw new Error("Point.fromHex: x=0 and x_0=1");
        if (isLastByteOdd !== isXOdd)
          x = modP2(-x);
        return Point2.fromAffine({ x, y });
      }
      static fromPrivateKey(privKey) {
        return getExtendedPublicKey(privKey).point;
      }
      toRawBytes() {
        const { x, y } = this.toAffine();
        const bytes2 = numberToBytesLE(y, Fp8.BYTES);
        bytes2[bytes2.length - 1] |= x & _1n6 ? 128 : 0;
        return bytes2;
      }
      toHex() {
        return bytesToHex(this.toRawBytes());
      }
    }
    Point2.BASE = new Point2(CURVE2.Gx, CURVE2.Gy, _1n6, modP2(CURVE2.Gx * CURVE2.Gy));
    Point2.ZERO = new Point2(_0n6, _1n6, _1n6, _0n6);
    const { BASE: G, ZERO: I } = Point2;
    const wnaf = wNAF(Point2, nByteLength * 8);
    function modN2(a) {
      return mod(a, CURVE_ORDER);
    }
    function modN_LE(hash2) {
      return modN2(bytesToNumberLE(hash2));
    }
    function getExtendedPublicKey(key) {
      const len = nByteLength;
      key = ensureBytes("private key", key, len);
      const hashed = ensureBytes("hashed private key", cHash(key), 2 * len);
      const head = adjustScalarBytes3(hashed.slice(0, len));
      const prefix = hashed.slice(len, 2 * len);
      const scalar = modN_LE(head);
      const point = G.multiply(scalar);
      const pointBytes = point.toRawBytes();
      return { head, prefix, scalar, point, pointBytes };
    }
    function getPublicKey(privKey) {
      return getExtendedPublicKey(privKey).pointBytes;
    }
    function hashDomainToScalar(context = new Uint8Array(), ...msgs) {
      const msg = concatBytes(...msgs);
      return modN_LE(cHash(domain(msg, ensureBytes("context", context), !!prehash)));
    }
    function sign(msg, privKey, options = {}) {
      msg = ensureBytes("message", msg);
      if (prehash)
        msg = prehash(msg);
      const { prefix, scalar, pointBytes } = getExtendedPublicKey(privKey);
      const r = hashDomainToScalar(options.context, prefix, msg);
      const R = G.multiply(r).toRawBytes();
      const k = hashDomainToScalar(options.context, R, pointBytes, msg);
      const s = modN2(r + k * scalar);
      assertGE0(s);
      const res = concatBytes(R, numberToBytesLE(s, Fp8.BYTES));
      return ensureBytes("result", res, nByteLength * 2);
    }
    const verifyOpts = VERIFY_DEFAULT;
    function verify(sig, msg, publicKey, options = verifyOpts) {
      const { context, zip215 } = options;
      const len = Fp8.BYTES;
      sig = ensureBytes("signature", sig, 2 * len);
      msg = ensureBytes("message", msg);
      if (prehash)
        msg = prehash(msg);
      const s = bytesToNumberLE(sig.slice(len, 2 * len));
      let A, R, SB;
      try {
        A = Point2.fromHex(publicKey, zip215);
        R = Point2.fromHex(sig.slice(0, len), zip215);
        SB = G.multiplyUnsafe(s);
      } catch (error) {
        return false;
      }
      if (!zip215 && A.isSmallOrder())
        return false;
      const k = hashDomainToScalar(context, R.toRawBytes(), A.toRawBytes(), msg);
      const RkA = R.add(A.multiplyUnsafe(k));
      return RkA.subtract(SB).clearCofactor().equals(Point2.ZERO);
    }
    G._setWindowSize(8);
    const utils2 = {
      getExtendedPublicKey,
      // ed25519 private keys are uniform 32b. No need to check for modulo bias, like in secp256k1.
      randomPrivateKey: () => randomBytes2(Fp8.BYTES),
      /**
       * We're doing scalar multiplication (used in getPublicKey etc) with precomputed BASE_POINT
       * values. This slows down first getPublicKey() by milliseconds (see Speed section),
       * but allows to speed-up subsequent getPublicKey() calls up to 20x.
       * @param windowSize 2, 4, 8, 16
       */
      precompute(windowSize = 8, point = Point2.BASE) {
        point._setWindowSize(windowSize);
        point.multiply(BigInt(3));
        return point;
      }
    };
    return {
      CURVE: CURVE2,
      getPublicKey,
      sign,
      verify,
      ExtendedPoint: Point2,
      utils: utils2
    };
  }

  // ../esm/abstract/montgomery.js
  var _0n7 = BigInt(0);
  var _1n7 = BigInt(1);
  function validateOpts3(curve) {
    validateObject(curve, {
      a: "bigint"
    }, {
      montgomeryBits: "isSafeInteger",
      nByteLength: "isSafeInteger",
      adjustScalarBytes: "function",
      domain: "function",
      powPminus2: "function",
      Gu: "bigint"
    });
    return Object.freeze({ ...curve });
  }
  function montgomery(curveDef) {
    const CURVE2 = validateOpts3(curveDef);
    const { P: P3 } = CURVE2;
    const modP2 = (n) => mod(n, P3);
    const montgomeryBits = CURVE2.montgomeryBits;
    const montgomeryBytes = Math.ceil(montgomeryBits / 8);
    const fieldLen = CURVE2.nByteLength;
    const adjustScalarBytes3 = CURVE2.adjustScalarBytes || ((bytes2) => bytes2);
    const powPminus2 = CURVE2.powPminus2 || ((x) => pow(x, P3 - BigInt(2), P3));
    function cswap(swap, x_2, x_3) {
      const dummy = modP2(swap * (x_2 - x_3));
      x_2 = modP2(x_2 - dummy);
      x_3 = modP2(x_3 + dummy);
      return [x_2, x_3];
    }
    function assertFieldElement(n) {
      if (typeof n === "bigint" && _0n7 <= n && n < P3)
        return n;
      throw new Error("Expected valid scalar 0 < scalar < CURVE.P");
    }
    const a24 = (CURVE2.a - BigInt(2)) / BigInt(4);
    function montgomeryLadder(pointU, scalar) {
      const u = assertFieldElement(pointU);
      const k = assertFieldElement(scalar);
      const x_1 = u;
      let x_2 = _1n7;
      let z_2 = _0n7;
      let x_3 = u;
      let z_3 = _1n7;
      let swap = _0n7;
      let sw;
      for (let t = BigInt(montgomeryBits - 1); t >= _0n7; t--) {
        const k_t = k >> t & _1n7;
        swap ^= k_t;
        sw = cswap(swap, x_2, x_3);
        x_2 = sw[0];
        x_3 = sw[1];
        sw = cswap(swap, z_2, z_3);
        z_2 = sw[0];
        z_3 = sw[1];
        swap = k_t;
        const A = x_2 + z_2;
        const AA = modP2(A * A);
        const B = x_2 - z_2;
        const BB = modP2(B * B);
        const E = AA - BB;
        const C = x_3 + z_3;
        const D = x_3 - z_3;
        const DA = modP2(D * A);
        const CB = modP2(C * B);
        const dacb = DA + CB;
        const da_cb = DA - CB;
        x_3 = modP2(dacb * dacb);
        z_3 = modP2(x_1 * modP2(da_cb * da_cb));
        x_2 = modP2(AA * BB);
        z_2 = modP2(E * (AA + modP2(a24 * E)));
      }
      sw = cswap(swap, x_2, x_3);
      x_2 = sw[0];
      x_3 = sw[1];
      sw = cswap(swap, z_2, z_3);
      z_2 = sw[0];
      z_3 = sw[1];
      const z2 = powPminus2(z_2);
      return modP2(x_2 * z2);
    }
    function encodeUCoordinate(u) {
      return numberToBytesLE(modP2(u), montgomeryBytes);
    }
    function decodeUCoordinate(uEnc) {
      const u = ensureBytes("u coordinate", uEnc, montgomeryBytes);
      if (fieldLen === 32)
        u[31] &= 127;
      return bytesToNumberLE(u);
    }
    function decodeScalar(n) {
      const bytes2 = ensureBytes("scalar", n);
      const len = bytes2.length;
      if (len !== montgomeryBytes && len !== fieldLen)
        throw new Error(`Expected ${montgomeryBytes} or ${fieldLen} bytes, got ${len}`);
      return bytesToNumberLE(adjustScalarBytes3(bytes2));
    }
    function scalarMult(scalar, u) {
      const pointU = decodeUCoordinate(u);
      const _scalar = decodeScalar(scalar);
      const pu = montgomeryLadder(pointU, _scalar);
      if (pu === _0n7)
        throw new Error("Invalid private or public key received");
      return encodeUCoordinate(pu);
    }
    const GuBytes = encodeUCoordinate(CURVE2.Gu);
    function scalarMultBase(scalar) {
      return scalarMult(scalar, GuBytes);
    }
    return {
      scalarMult,
      scalarMultBase,
      getSharedSecret: (privateKey, publicKey) => scalarMult(privateKey, publicKey),
      getPublicKey: (privateKey) => scalarMultBase(privateKey),
      utils: { randomPrivateKey: () => CURVE2.randomBytes(CURVE2.nByteLength) },
      GuBytes
    };
  }

  // ../esm/ed25519.js
  var ED25519_P = BigInt("57896044618658097711785492504343953926634992332820282019728792003956564819949");
  var ED25519_SQRT_M1 = BigInt("19681161376707505956807079304988542015446066515923890162744021073123829784752");
  var _0n8 = BigInt(0);
  var _1n8 = BigInt(1);
  var _2n6 = BigInt(2);
  var _5n2 = BigInt(5);
  var _10n = BigInt(10);
  var _20n = BigInt(20);
  var _40n = BigInt(40);
  var _80n = BigInt(80);
  function ed25519_pow_2_252_3(x) {
    const P3 = ED25519_P;
    const x2 = x * x % P3;
    const b2 = x2 * x % P3;
    const b4 = pow2(b2, _2n6, P3) * b2 % P3;
    const b5 = pow2(b4, _1n8, P3) * x % P3;
    const b10 = pow2(b5, _5n2, P3) * b5 % P3;
    const b20 = pow2(b10, _10n, P3) * b10 % P3;
    const b40 = pow2(b20, _20n, P3) * b20 % P3;
    const b80 = pow2(b40, _40n, P3) * b40 % P3;
    const b160 = pow2(b80, _80n, P3) * b80 % P3;
    const b240 = pow2(b160, _80n, P3) * b80 % P3;
    const b250 = pow2(b240, _10n, P3) * b10 % P3;
    const pow_p_5_8 = pow2(b250, _2n6, P3) * x % P3;
    return { pow_p_5_8, b2 };
  }
  function adjustScalarBytes(bytes2) {
    bytes2[0] &= 248;
    bytes2[31] &= 127;
    bytes2[31] |= 64;
    return bytes2;
  }
  function uvRatio(u, v) {
    const P3 = ED25519_P;
    const v3 = mod(v * v * v, P3);
    const v7 = mod(v3 * v3 * v, P3);
    const pow3 = ed25519_pow_2_252_3(u * v7).pow_p_5_8;
    let x = mod(u * v3 * pow3, P3);
    const vx2 = mod(v * x * x, P3);
    const root1 = x;
    const root2 = mod(x * ED25519_SQRT_M1, P3);
    const useRoot1 = vx2 === u;
    const useRoot2 = vx2 === mod(-u, P3);
    const noRoot = vx2 === mod(-u * ED25519_SQRT_M1, P3);
    if (useRoot1)
      x = root1;
    if (useRoot2 || noRoot)
      x = root2;
    if (isNegativeLE(x, P3))
      x = mod(-x, P3);
    return { isValid: useRoot1 || useRoot2, value: x };
  }
  var Fp2 = Field(ED25519_P, void 0, true);
  var ed25519Defaults = {
    // Param: a
    a: BigInt(-1),
    // Fp.create(-1) is proper; our way still works and is faster
    // d is equal to -121665/121666 over finite field.
    // Negative number is P - number, and division is invert(number, P)
    d: BigInt("37095705934669439343138083508754565189542113879843219016388785533085940283555"),
    // Finite field 𝔽p over which we'll do calculations; 2n**255n - 19n
    Fp: Fp2,
    // Subgroup order: how many points curve has
    // 2n**252n + 27742317777372353535851937790883648493n;
    n: BigInt("7237005577332262213973186563042994240857116359379907606001950938285454250989"),
    // Cofactor
    h: BigInt(8),
    // Base point (x, y) aka generator point
    Gx: BigInt("15112221349535400772501151409588531511454012693041857206046113283949847762202"),
    Gy: BigInt("46316835694926478169428394003475163141307993866256225615783033603165251855960"),
    hash: sha512,
    randomBytes,
    adjustScalarBytes,
    // dom2
    // Ratio of u to v. Allows us to combine inversion and square root. Uses algo from RFC8032 5.1.3.
    // Constant-time, u/√v
    uvRatio
  };
  var ed25519 = /* @__PURE__ */ twistedEdwards(ed25519Defaults);
  function ed25519_domain(data, ctx, phflag) {
    if (ctx.length > 255)
      throw new Error("Context is too big");
    return concatBytes2(utf8ToBytes2("SigEd25519 no Ed25519 collisions"), new Uint8Array([phflag ? 1 : 0, ctx.length]), ctx, data);
  }
  var ed25519ctx = /* @__PURE__ */ twistedEdwards({
    ...ed25519Defaults,
    domain: ed25519_domain
  });
  var ed25519ph = /* @__PURE__ */ twistedEdwards({
    ...ed25519Defaults,
    domain: ed25519_domain,
    prehash: sha512
  });
  var x25519 = /* @__PURE__ */ (() => montgomery({
    P: ED25519_P,
    a: BigInt(486662),
    montgomeryBits: 255,
    // n is 253 bits
    nByteLength: 32,
    Gu: BigInt(9),
    powPminus2: (x) => {
      const P3 = ED25519_P;
      const { pow_p_5_8, b2 } = ed25519_pow_2_252_3(x);
      return mod(pow2(pow_p_5_8, BigInt(3), P3) * b2, P3);
    },
    adjustScalarBytes,
    randomBytes
  }))();
  function edwardsToMontgomeryPub(edwardsPub) {
    const { y } = ed25519.ExtendedPoint.fromHex(edwardsPub);
    const _1n12 = BigInt(1);
    return Fp2.toBytes(Fp2.create((_1n12 + y) * Fp2.inv(_1n12 - y)));
  }
  function edwardsToMontgomeryPriv(edwardsPriv) {
    const hashed = ed25519Defaults.hash(edwardsPriv.subarray(0, 32));
    return ed25519Defaults.adjustScalarBytes(hashed).subarray(0, 32);
  }
  var ELL2_C1 = (Fp2.ORDER + BigInt(3)) / BigInt(8);
  var ELL2_C2 = Fp2.pow(_2n6, ELL2_C1);
  var ELL2_C3 = Fp2.sqrt(Fp2.neg(Fp2.ONE));
  var ELL2_C4 = (Fp2.ORDER - BigInt(5)) / BigInt(8);
  var ELL2_J = BigInt(486662);
  var ELL2_C1_EDWARDS = FpSqrtEven(Fp2, Fp2.neg(BigInt(486664)));
  var SQRT_AD_MINUS_ONE = BigInt("25063068953384623474111414158702152701244531502492656460079210482610430750235");
  var INVSQRT_A_MINUS_D = BigInt("54469307008909316920995813868745141605393597292927456921205312896311721017578");
  var ONE_MINUS_D_SQ = BigInt("1159843021668779879193775521855586647937357759715417654439879720876111806838");
  var D_MINUS_ONE_SQ = BigInt("40440834346308536858101042469323190826248399146238708352240133220865137265952");
  var MAX_255B = BigInt("0x7fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff");

  // ../node_modules/@noble/hashes/esm/sha3.js
  var SHA3_PI = [];
  var SHA3_ROTL = [];
  var _SHA3_IOTA = [];
  var _0n9 = /* @__PURE__ */ BigInt(0);
  var _1n9 = /* @__PURE__ */ BigInt(1);
  var _2n7 = /* @__PURE__ */ BigInt(2);
  var _7n = /* @__PURE__ */ BigInt(7);
  var _256n = /* @__PURE__ */ BigInt(256);
  var _0x71n = /* @__PURE__ */ BigInt(113);
  for (let round = 0, R = _1n9, x = 1, y = 0; round < 24; round++) {
    [x, y] = [y, (2 * x + 3 * y) % 5];
    SHA3_PI.push(2 * (5 * y + x));
    SHA3_ROTL.push((round + 1) * (round + 2) / 2 % 64);
    let t = _0n9;
    for (let j = 0; j < 7; j++) {
      R = (R << _1n9 ^ (R >> _7n) * _0x71n) % _256n;
      if (R & _2n7)
        t ^= _1n9 << (_1n9 << /* @__PURE__ */ BigInt(j)) - _1n9;
    }
    _SHA3_IOTA.push(t);
  }
  var [SHA3_IOTA_H, SHA3_IOTA_L] = /* @__PURE__ */ split(_SHA3_IOTA, true);
  var rotlH = (h, l, s) => s > 32 ? rotlBH(h, l, s) : rotlSH(h, l, s);
  var rotlL = (h, l, s) => s > 32 ? rotlBL(h, l, s) : rotlSL(h, l, s);
  function keccakP(s, rounds = 24) {
    const B = new Uint32Array(5 * 2);
    for (let round = 24 - rounds; round < 24; round++) {
      for (let x = 0; x < 10; x++)
        B[x] = s[x] ^ s[x + 10] ^ s[x + 20] ^ s[x + 30] ^ s[x + 40];
      for (let x = 0; x < 10; x += 2) {
        const idx1 = (x + 8) % 10;
        const idx0 = (x + 2) % 10;
        const B0 = B[idx0];
        const B1 = B[idx0 + 1];
        const Th = rotlH(B0, B1, 1) ^ B[idx1];
        const Tl = rotlL(B0, B1, 1) ^ B[idx1 + 1];
        for (let y = 0; y < 50; y += 10) {
          s[x + y] ^= Th;
          s[x + y + 1] ^= Tl;
        }
      }
      let curH = s[2];
      let curL = s[3];
      for (let t = 0; t < 24; t++) {
        const shift = SHA3_ROTL[t];
        const Th = rotlH(curH, curL, shift);
        const Tl = rotlL(curH, curL, shift);
        const PI = SHA3_PI[t];
        curH = s[PI];
        curL = s[PI + 1];
        s[PI] = Th;
        s[PI + 1] = Tl;
      }
      for (let y = 0; y < 50; y += 10) {
        for (let x = 0; x < 10; x++)
          B[x] = s[y + x];
        for (let x = 0; x < 10; x++)
          s[y + x] ^= ~B[(x + 2) % 10] & B[(x + 4) % 10];
      }
      s[0] ^= SHA3_IOTA_H[round];
      s[1] ^= SHA3_IOTA_L[round];
    }
    B.fill(0);
  }
  var Keccak = class _Keccak extends Hash {
    // NOTE: we accept arguments in bytes instead of bits here.
    constructor(blockLen, suffix, outputLen, enableXOF = false, rounds = 24) {
      super();
      this.blockLen = blockLen;
      this.suffix = suffix;
      this.outputLen = outputLen;
      this.enableXOF = enableXOF;
      this.rounds = rounds;
      this.pos = 0;
      this.posOut = 0;
      this.finished = false;
      this.destroyed = false;
      number(outputLen);
      if (0 >= this.blockLen || this.blockLen >= 200)
        throw new Error("Sha3 supports only keccak-f1600 function");
      this.state = new Uint8Array(200);
      this.state32 = u32(this.state);
    }
    keccak() {
      if (!isLE)
        byteSwap32(this.state32);
      keccakP(this.state32, this.rounds);
      if (!isLE)
        byteSwap32(this.state32);
      this.posOut = 0;
      this.pos = 0;
    }
    update(data) {
      exists(this);
      const { blockLen, state } = this;
      data = toBytes(data);
      const len = data.length;
      for (let pos = 0; pos < len; ) {
        const take = Math.min(blockLen - this.pos, len - pos);
        for (let i = 0; i < take; i++)
          state[this.pos++] ^= data[pos++];
        if (this.pos === blockLen)
          this.keccak();
      }
      return this;
    }
    finish() {
      if (this.finished)
        return;
      this.finished = true;
      const { state, suffix, pos, blockLen } = this;
      state[pos] ^= suffix;
      if ((suffix & 128) !== 0 && pos === blockLen - 1)
        this.keccak();
      state[blockLen - 1] ^= 128;
      this.keccak();
    }
    writeInto(out) {
      exists(this, false);
      bytes(out);
      this.finish();
      const bufferOut = this.state;
      const { blockLen } = this;
      for (let pos = 0, len = out.length; pos < len; ) {
        if (this.posOut >= blockLen)
          this.keccak();
        const take = Math.min(blockLen - this.posOut, len - pos);
        out.set(bufferOut.subarray(this.posOut, this.posOut + take), pos);
        this.posOut += take;
        pos += take;
      }
      return out;
    }
    xofInto(out) {
      if (!this.enableXOF)
        throw new Error("XOF is not possible for this instance");
      return this.writeInto(out);
    }
    xof(bytes2) {
      number(bytes2);
      return this.xofInto(new Uint8Array(bytes2));
    }
    digestInto(out) {
      output(out, this);
      if (this.finished)
        throw new Error("digest() was already called");
      this.writeInto(out);
      this.destroy();
      return out;
    }
    digest() {
      return this.digestInto(new Uint8Array(this.outputLen));
    }
    destroy() {
      this.destroyed = true;
      this.state.fill(0);
    }
    _cloneInto(to) {
      const { blockLen, suffix, outputLen, rounds, enableXOF } = this;
      to || (to = new _Keccak(blockLen, suffix, outputLen, enableXOF, rounds));
      to.state32.set(this.state32);
      to.pos = this.pos;
      to.posOut = this.posOut;
      to.finished = this.finished;
      to.rounds = rounds;
      to.suffix = suffix;
      to.outputLen = outputLen;
      to.enableXOF = enableXOF;
      to.destroyed = this.destroyed;
      return to;
    }
  };
  var gen = (suffix, blockLen, outputLen) => wrapConstructor(() => new Keccak(blockLen, suffix, outputLen));
  var sha3_224 = /* @__PURE__ */ gen(6, 144, 224 / 8);
  var sha3_256 = /* @__PURE__ */ gen(6, 136, 256 / 8);
  var sha3_384 = /* @__PURE__ */ gen(6, 104, 384 / 8);
  var sha3_512 = /* @__PURE__ */ gen(6, 72, 512 / 8);
  var keccak_224 = /* @__PURE__ */ gen(1, 144, 224 / 8);
  var keccak_256 = /* @__PURE__ */ gen(1, 136, 256 / 8);
  var keccak_384 = /* @__PURE__ */ gen(1, 104, 384 / 8);
  var keccak_512 = /* @__PURE__ */ gen(1, 72, 512 / 8);
  var genShake = (suffix, blockLen, outputLen) => wrapXOFConstructorWithOpts((opts = {}) => new Keccak(blockLen, suffix, opts.dkLen === void 0 ? outputLen : opts.dkLen, true));
  var shake128 = /* @__PURE__ */ genShake(31, 168, 128 / 8);
  var shake256 = /* @__PURE__ */ genShake(31, 136, 256 / 8);

  // ../esm/ed448.js
  var shake256_114 = wrapConstructor(() => shake256.create({ dkLen: 114 }));
  var shake256_64 = wrapConstructor(() => shake256.create({ dkLen: 64 }));
  var ed448P = BigInt("726838724295606890549323807888004534353641360687318060281490199180612328166730772686396383698676545930088884461843637361053498018365439");
  var _1n10 = BigInt(1);
  var _2n8 = BigInt(2);
  var _3n3 = BigInt(3);
  var _4n3 = BigInt(4);
  var _11n = BigInt(11);
  var _22n = BigInt(22);
  var _44n = BigInt(44);
  var _88n = BigInt(88);
  var _223n = BigInt(223);
  function ed448_pow_Pminus3div4(x) {
    const P3 = ed448P;
    const b2 = x * x * x % P3;
    const b3 = b2 * b2 * x % P3;
    const b6 = pow2(b3, _3n3, P3) * b3 % P3;
    const b9 = pow2(b6, _3n3, P3) * b3 % P3;
    const b11 = pow2(b9, _2n8, P3) * b2 % P3;
    const b22 = pow2(b11, _11n, P3) * b11 % P3;
    const b44 = pow2(b22, _22n, P3) * b22 % P3;
    const b88 = pow2(b44, _44n, P3) * b44 % P3;
    const b176 = pow2(b88, _88n, P3) * b88 % P3;
    const b220 = pow2(b176, _44n, P3) * b44 % P3;
    const b222 = pow2(b220, _2n8, P3) * b2 % P3;
    const b223 = pow2(b222, _1n10, P3) * x % P3;
    return pow2(b223, _223n, P3) * b222 % P3;
  }
  function adjustScalarBytes2(bytes2) {
    bytes2[0] &= 252;
    bytes2[55] |= 128;
    bytes2[56] = 0;
    return bytes2;
  }
  function uvRatio2(u, v) {
    const P3 = ed448P;
    const u2v = mod(u * u * v, P3);
    const u3v = mod(u2v * u, P3);
    const u5v3 = mod(u3v * u2v * v, P3);
    const root = ed448_pow_Pminus3div4(u5v3);
    const x = mod(u3v * root, P3);
    const x2 = mod(x * x, P3);
    return { isValid: mod(x2 * v, P3) === u, value: x };
  }
  var Fp3 = Field(ed448P, 456, true);
  var ED448_DEF = {
    // Param: a
    a: BigInt(1),
    // -39081. Negative number is P - number
    d: BigInt("726838724295606890549323807888004534353641360687318060281490199180612328166730772686396383698676545930088884461843637361053498018326358"),
    // Finite field 𝔽p over which we'll do calculations; 2n**448n - 2n**224n - 1n
    Fp: Fp3,
    // Subgroup order: how many points curve has;
    // 2n**446n - 13818066809895115352007386748515426880336692474882178609894547503885n
    n: BigInt("181709681073901722637330951972001133588410340171829515070372549795146003961539585716195755291692375963310293709091662304773755859649779"),
    // RFC 7748 has 56-byte keys, RFC 8032 has 57-byte keys
    nBitLength: 456,
    // Cofactor
    h: BigInt(4),
    // Base point (x, y) aka generator point
    Gx: BigInt("224580040295924300187604334099896036246789641632564134246125461686950415467406032909029192869357953282578032075146446173674602635247710"),
    Gy: BigInt("298819210078481492676017930443930673437544040154080242095928241372331506189835876003536878655418784733982303233503462500531545062832660"),
    // SHAKE256(dom4(phflag,context)||x, 114)
    hash: shake256_114,
    randomBytes,
    adjustScalarBytes: adjustScalarBytes2,
    // dom4
    domain: (data, ctx, phflag) => {
      if (ctx.length > 255)
        throw new Error(`Context is too big: ${ctx.length}`);
      return concatBytes2(utf8ToBytes2("SigEd448"), new Uint8Array([phflag ? 1 : 0, ctx.length]), ctx, data);
    },
    uvRatio: uvRatio2
  };
  var ed448 = /* @__PURE__ */ twistedEdwards(ED448_DEF);
  var ed448ph = /* @__PURE__ */ twistedEdwards({ ...ED448_DEF, prehash: shake256_64 });
  var x448 = /* @__PURE__ */ (() => montgomery({
    a: BigInt(156326),
    // RFC 7748 has 56-byte keys, RFC 8032 has 57-byte keys
    montgomeryBits: 448,
    nByteLength: 56,
    P: ed448P,
    Gu: BigInt(5),
    powPminus2: (x) => {
      const P3 = ed448P;
      const Pminus3div4 = ed448_pow_Pminus3div4(x);
      const Pminus3 = pow2(Pminus3div4, BigInt(2), P3);
      return mod(Pminus3 * x, P3);
    },
    adjustScalarBytes: adjustScalarBytes2,
    randomBytes
  }))();
  function edwardsToMontgomeryPub2(edwardsPub) {
    const { y } = ed448.ExtendedPoint.fromHex(edwardsPub);
    const _1n12 = BigInt(1);
    return Fp3.toBytes(Fp3.create((y - _1n12) * Fp3.inv(y + _1n12)));
  }
  var ELL2_C12 = (Fp3.ORDER - BigInt(3)) / BigInt(4);
  var ELL2_J2 = BigInt(156326);
  var ONE_MINUS_D = BigInt("39082");
  var ONE_MINUS_TWO_D = BigInt("78163");
  var SQRT_MINUS_D = BigInt("98944233647732219769177004876929019128417576295529901074099889598043702116001257856802131563896515373927712232092845883226922417596214");
  var INVSQRT_MINUS_D = BigInt("315019913931389607337177038330951043522456072897266928557328499619017160722351061360252776265186336876723201881398623946864393857820716");
  var MAX_448B = BigInt("0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff");

  // ../esm/p256.js
  var Fp4 = Field(BigInt("0xffffffff00000001000000000000000000000000ffffffffffffffffffffffff"));
  var CURVE_A = Fp4.create(BigInt("-3"));
  var CURVE_B = BigInt("0x5ac635d8aa3a93e7b3ebbd55769886bc651d06b0cc53b0f63bce3c3e27d2604b");
  var p256 = createCurve({
    a: CURVE_A,
    // Equation params: a, b
    b: CURVE_B,
    Fp: Fp4,
    // Field: 2n**224n * (2n**32n-1n) + 2n**192n + 2n**96n-1n
    // Curve order, total count of valid points in the field
    n: BigInt("0xffffffff00000000ffffffffffffffffbce6faada7179e84f3b9cac2fc632551"),
    // Base (generator) point (x, y)
    Gx: BigInt("0x6b17d1f2e12c4247f8bce6e563a440f277037d812deb33a0f4a13945d898c296"),
    Gy: BigInt("0x4fe342e2fe1a7f9b8ee7eb4a7c0f9e162bce33576b315ececbb6406837bf51f5"),
    h: BigInt(1),
    lowS: false
  }, sha256);

  // ../esm/p384.js
  var P = BigInt("0xfffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffeffffffff0000000000000000ffffffff");
  var Fp5 = Field(P);
  var CURVE_A2 = Fp5.create(BigInt("-3"));
  var CURVE_B2 = BigInt("0xb3312fa7e23ee7e4988e056be3f82d19181d9c6efe8141120314088f5013875ac656398d8a2ed19d2a85c8edd3ec2aef");
  var p384 = createCurve({
    a: CURVE_A2,
    // Equation params: a, b
    b: CURVE_B2,
    Fp: Fp5,
    // Field: 2n**384n - 2n**128n - 2n**96n + 2n**32n - 1n
    // Curve order, total count of valid points in the field.
    n: BigInt("0xffffffffffffffffffffffffffffffffffffffffffffffffc7634d81f4372ddf581a0db248b0a77aecec196accc52973"),
    // Base (generator) point (x, y)
    Gx: BigInt("0xaa87ca22be8b05378eb1c71ef320ad746e1d3b628ba79b9859f741e082542a385502f25dbf55296c3a545e3872760ab7"),
    Gy: BigInt("0x3617de4a96262c6f5d9e98bf9292dc29f8f41dbd289a147ce9da3113b5f0b8c00a60b1ce1d7e819d7a431d7c90ea0e5f"),
    h: BigInt(1),
    lowS: false
  }, sha384);

  // ../esm/p521.js
  var P2 = BigInt("0x1ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff");
  var Fp6 = Field(P2);
  var CURVE = {
    a: Fp6.create(BigInt("-3")),
    b: BigInt("0x0051953eb9618e1c9a1f929a21a0b68540eea2da725b99b315f3b8b489918ef109e156193951ec7e937b1652c0bd3bb1bf073573df883d2c34f1ef451fd46b503f00"),
    Fp: Fp6,
    n: BigInt("0x01fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffa51868783bf2f966b7fcc0148f709a5d03bb5c9b8899c47aebb6fb71e91386409"),
    Gx: BigInt("0x00c6858e06b70404e9cd9e3ecb662395b4429c648139053fb521f828af606b4d3dbaa14b5e77efe75928fe1dc127a2ffa8de3348b3c1856a429bf97e7e31c2e5bd66"),
    Gy: BigInt("0x011839296a789a3bc0045c8a5fb42c7d1bd998f54449579b446817afbd17273e662c97ee72995ef42640c550b9013fad0761353c7086a272c24088be94769fd16650"),
    h: BigInt(1)
  };
  var p521 = createCurve({
    a: CURVE.a,
    // Equation params: a, b
    b: CURVE.b,
    Fp: Fp6,
    // Field: 2n**521n - 1n
    // Curve order, total count of valid points in the field
    n: CURVE.n,
    Gx: CURVE.Gx,
    // Base point (x, y) aka generator point
    Gy: CURVE.Gy,
    h: CURVE.h,
    lowS: false,
    allowedPrivateKeyLengths: [130, 131, 132]
    // P521 keys are variable-length. Normalize to 132b
  }, sha512);

  // ../esm/abstract/bls.js
  var _2n9 = BigInt(2);
  var _3n4 = BigInt(3);
  function bls(CURVE2) {
    const { Fp: Fp8, Fr: Fr2, Fp2: Fp23, Fp6: Fp63, Fp12: Fp122 } = CURVE2.fields;
    const BLS_X_LEN2 = bitLen(CURVE2.params.x);
    function calcPairingPrecomputes(p) {
      const { x, y } = p;
      const Qx = x, Qy = y, Qz = Fp23.ONE;
      let Rx = Qx, Ry = Qy, Rz = Qz;
      let ell_coeff = [];
      for (let i = BLS_X_LEN2 - 2; i >= 0; i--) {
        let t0 = Fp23.sqr(Ry);
        let t1 = Fp23.sqr(Rz);
        let t2 = Fp23.multiplyByB(Fp23.mul(t1, _3n4));
        let t3 = Fp23.mul(t2, _3n4);
        let t4 = Fp23.sub(Fp23.sub(Fp23.sqr(Fp23.add(Ry, Rz)), t1), t0);
        ell_coeff.push([
          Fp23.sub(t2, t0),
          // T2 - T0
          Fp23.mul(Fp23.sqr(Rx), _3n4),
          // 3 * Rx²
          Fp23.neg(t4)
          // -T4
        ]);
        Rx = Fp23.div(Fp23.mul(Fp23.mul(Fp23.sub(t0, t3), Rx), Ry), _2n9);
        Ry = Fp23.sub(Fp23.sqr(Fp23.div(Fp23.add(t0, t3), _2n9)), Fp23.mul(Fp23.sqr(t2), _3n4));
        Rz = Fp23.mul(t0, t4);
        if (bitGet(CURVE2.params.x, i)) {
          let t02 = Fp23.sub(Ry, Fp23.mul(Qy, Rz));
          let t12 = Fp23.sub(Rx, Fp23.mul(Qx, Rz));
          ell_coeff.push([
            Fp23.sub(Fp23.mul(t02, Qx), Fp23.mul(t12, Qy)),
            // T0 * Qx - T1 * Qy
            Fp23.neg(t02),
            // -T0
            t12
            // T1
          ]);
          let t22 = Fp23.sqr(t12);
          let t32 = Fp23.mul(t22, t12);
          let t42 = Fp23.mul(t22, Rx);
          let t5 = Fp23.add(Fp23.sub(t32, Fp23.mul(t42, _2n9)), Fp23.mul(Fp23.sqr(t02), Rz));
          Rx = Fp23.mul(t12, t5);
          Ry = Fp23.sub(Fp23.mul(Fp23.sub(t42, t5), t02), Fp23.mul(t32, Ry));
          Rz = Fp23.mul(Rz, t32);
        }
      }
      return ell_coeff;
    }
    function millerLoop(ell, g1) {
      const { x } = CURVE2.params;
      const Px = g1[0];
      const Py = g1[1];
      let f12 = Fp122.ONE;
      for (let j = 0, i = BLS_X_LEN2 - 2; i >= 0; i--, j++) {
        const E = ell[j];
        f12 = Fp122.multiplyBy014(f12, E[0], Fp23.mul(E[1], Px), Fp23.mul(E[2], Py));
        if (bitGet(x, i)) {
          j += 1;
          const F = ell[j];
          f12 = Fp122.multiplyBy014(f12, F[0], Fp23.mul(F[1], Px), Fp23.mul(F[2], Py));
        }
        if (i !== 0)
          f12 = Fp122.sqr(f12);
      }
      return Fp122.conjugate(f12);
    }
    const utils2 = {
      randomPrivateKey: () => {
        const length = getMinHashLength(Fr2.ORDER);
        return mapHashToField(CURVE2.randomBytes(length), Fr2.ORDER);
      },
      calcPairingPrecomputes
    };
    const G1_ = weierstrassPoints({ n: Fr2.ORDER, ...CURVE2.G1 });
    const G1 = Object.assign(G1_, createHasher(G1_.ProjectivePoint, CURVE2.G1.mapToCurve, {
      ...CURVE2.htfDefaults,
      ...CURVE2.G1.htfDefaults
    }));
    function pairingPrecomputes(point) {
      const p = point;
      if (p._PPRECOMPUTES)
        return p._PPRECOMPUTES;
      p._PPRECOMPUTES = calcPairingPrecomputes(point.toAffine());
      return p._PPRECOMPUTES;
    }
    const G2_ = weierstrassPoints({ n: Fr2.ORDER, ...CURVE2.G2 });
    const G2 = Object.assign(G2_, createHasher(G2_.ProjectivePoint, CURVE2.G2.mapToCurve, {
      ...CURVE2.htfDefaults,
      ...CURVE2.G2.htfDefaults
    }));
    const { ShortSignature } = CURVE2.G1;
    const { Signature } = CURVE2.G2;
    function pairing(Q, P3, withFinalExponent = true) {
      if (Q.equals(G1.ProjectivePoint.ZERO) || P3.equals(G2.ProjectivePoint.ZERO))
        throw new Error("pairing is not available for ZERO point");
      Q.assertValidity();
      P3.assertValidity();
      const Qa = Q.toAffine();
      const looped = millerLoop(pairingPrecomputes(P3), [Qa.x, Qa.y]);
      return withFinalExponent ? Fp122.finalExponentiate(looped) : looped;
    }
    function normP1(point) {
      return point instanceof G1.ProjectivePoint ? point : G1.ProjectivePoint.fromHex(point);
    }
    function normP1Hash(point, htfOpts) {
      return point instanceof G1.ProjectivePoint ? point : G1.hashToCurve(ensureBytes("point", point), htfOpts);
    }
    function normP2(point) {
      return point instanceof G2.ProjectivePoint ? point : Signature.fromHex(point);
    }
    function normP2Hash(point, htfOpts) {
      return point instanceof G2.ProjectivePoint ? point : G2.hashToCurve(ensureBytes("point", point), htfOpts);
    }
    function getPublicKey(privateKey) {
      return G1.ProjectivePoint.fromPrivateKey(privateKey).toRawBytes(true);
    }
    function getPublicKeyForShortSignatures(privateKey) {
      return G2.ProjectivePoint.fromPrivateKey(privateKey).toRawBytes(true);
    }
    function sign(message, privateKey, htfOpts) {
      const msgPoint = normP2Hash(message, htfOpts);
      msgPoint.assertValidity();
      const sigPoint = msgPoint.multiply(G1.normPrivateKeyToScalar(privateKey));
      if (message instanceof G2.ProjectivePoint)
        return sigPoint;
      return Signature.toRawBytes(sigPoint);
    }
    function signShortSignature(message, privateKey, htfOpts) {
      const msgPoint = normP1Hash(message, htfOpts);
      msgPoint.assertValidity();
      const sigPoint = msgPoint.multiply(G1.normPrivateKeyToScalar(privateKey));
      if (message instanceof G1.ProjectivePoint)
        return sigPoint;
      return ShortSignature.toRawBytes(sigPoint);
    }
    function verify(signature, message, publicKey, htfOpts) {
      const P3 = normP1(publicKey);
      const Hm = normP2Hash(message, htfOpts);
      const G = G1.ProjectivePoint.BASE;
      const S = normP2(signature);
      const ePHm = pairing(P3.negate(), Hm, false);
      const eGS = pairing(G, S, false);
      const exp = Fp122.finalExponentiate(Fp122.mul(eGS, ePHm));
      return Fp122.eql(exp, Fp122.ONE);
    }
    function verifyShortSignature(signature, message, publicKey, htfOpts) {
      const P3 = normP2(publicKey);
      const Hm = normP1Hash(message, htfOpts);
      const G = G2.ProjectivePoint.BASE;
      const S = normP1(signature);
      const eHmP = pairing(Hm, P3, false);
      const eSG = pairing(S, G.negate(), false);
      const exp = Fp122.finalExponentiate(Fp122.mul(eSG, eHmP));
      return Fp122.eql(exp, Fp122.ONE);
    }
    function aggregatePublicKeys(publicKeys) {
      if (!publicKeys.length)
        throw new Error("Expected non-empty array");
      const agg = publicKeys.map(normP1).reduce((sum, p) => sum.add(p), G1.ProjectivePoint.ZERO);
      const aggAffine = agg;
      if (publicKeys[0] instanceof G1.ProjectivePoint) {
        aggAffine.assertValidity();
        return aggAffine;
      }
      return aggAffine.toRawBytes(true);
    }
    function aggregateSignatures(signatures) {
      if (!signatures.length)
        throw new Error("Expected non-empty array");
      const agg = signatures.map(normP2).reduce((sum, s) => sum.add(s), G2.ProjectivePoint.ZERO);
      const aggAffine = agg;
      if (signatures[0] instanceof G2.ProjectivePoint) {
        aggAffine.assertValidity();
        return aggAffine;
      }
      return Signature.toRawBytes(aggAffine);
    }
    function aggregateShortSignatures(signatures) {
      if (!signatures.length)
        throw new Error("Expected non-empty array");
      const agg = signatures.map(normP1).reduce((sum, s) => sum.add(s), G1.ProjectivePoint.ZERO);
      const aggAffine = agg;
      if (signatures[0] instanceof G1.ProjectivePoint) {
        aggAffine.assertValidity();
        return aggAffine;
      }
      return ShortSignature.toRawBytes(aggAffine);
    }
    function verifyBatch(signature, messages, publicKeys, htfOpts) {
      if (!messages.length)
        throw new Error("Expected non-empty messages array");
      if (publicKeys.length !== messages.length)
        throw new Error("Pubkey count should equal msg count");
      const sig = normP2(signature);
      const nMessages = messages.map((i) => normP2Hash(i, htfOpts));
      const nPublicKeys = publicKeys.map(normP1);
      try {
        const paired = [];
        for (const message of new Set(nMessages)) {
          const groupPublicKey = nMessages.reduce((groupPublicKey2, subMessage, i) => subMessage === message ? groupPublicKey2.add(nPublicKeys[i]) : groupPublicKey2, G1.ProjectivePoint.ZERO);
          paired.push(pairing(groupPublicKey, message, false));
        }
        paired.push(pairing(G1.ProjectivePoint.BASE.negate(), sig, false));
        const product = paired.reduce((a, b) => Fp122.mul(a, b), Fp122.ONE);
        const exp = Fp122.finalExponentiate(product);
        return Fp122.eql(exp, Fp122.ONE);
      } catch {
        return false;
      }
    }
    G1.ProjectivePoint.BASE._setWindowSize(4);
    return {
      getPublicKey,
      getPublicKeyForShortSignatures,
      sign,
      signShortSignature,
      verify,
      verifyBatch,
      verifyShortSignature,
      aggregatePublicKeys,
      aggregateSignatures,
      aggregateShortSignatures,
      millerLoop,
      pairing,
      G1,
      G2,
      Signature,
      ShortSignature,
      fields: {
        Fr: Fr2,
        Fp: Fp8,
        Fp2: Fp23,
        Fp6: Fp63,
        Fp12: Fp122
      },
      params: {
        x: CURVE2.params.x,
        r: CURVE2.params.r,
        G1b: CURVE2.G1.b,
        G2b: CURVE2.G2.b
      },
      utils: utils2
    };
  }

  // ../esm/bls12-381.js
  var _0n10 = BigInt(0);
  var _1n11 = BigInt(1);
  var _2n10 = BigInt(2);
  var _3n5 = BigInt(3);
  var _4n4 = BigInt(4);
  var _8n3 = BigInt(8);
  var _16n2 = BigInt(16);
  var Fp_raw = BigInt("0x1a0111ea397fe69a4b1ba7b6434bacd764774b84f38512bf6730d2a0f6b0f6241eabfffeb153ffffb9feffffffffaaab");
  var Fp7 = Field(Fp_raw);
  var Fr = Field(BigInt("0x73eda753299d7d483339d80809a1d80553bda402fffe5bfeffffffff00000001"));
  var Fp2Add = ({ c0, c1 }, { c0: r0, c1: r1 }) => ({
    c0: Fp7.add(c0, r0),
    c1: Fp7.add(c1, r1)
  });
  var Fp2Subtract = ({ c0, c1 }, { c0: r0, c1: r1 }) => ({
    c0: Fp7.sub(c0, r0),
    c1: Fp7.sub(c1, r1)
  });
  var Fp2Multiply = ({ c0, c1 }, rhs) => {
    if (typeof rhs === "bigint")
      return { c0: Fp7.mul(c0, rhs), c1: Fp7.mul(c1, rhs) };
    const { c0: r0, c1: r1 } = rhs;
    let t1 = Fp7.mul(c0, r0);
    let t2 = Fp7.mul(c1, r1);
    const o0 = Fp7.sub(t1, t2);
    const o1 = Fp7.sub(Fp7.mul(Fp7.add(c0, c1), Fp7.add(r0, r1)), Fp7.add(t1, t2));
    return { c0: o0, c1: o1 };
  };
  var Fp2Square = ({ c0, c1 }) => {
    const a = Fp7.add(c0, c1);
    const b = Fp7.sub(c0, c1);
    const c = Fp7.add(c0, c0);
    return { c0: Fp7.mul(a, b), c1: Fp7.mul(c, c1) };
  };
  var FP2_ORDER = Fp_raw * Fp_raw;
  var Fp22 = {
    ORDER: FP2_ORDER,
    BITS: bitLen(FP2_ORDER),
    BYTES: Math.ceil(bitLen(FP2_ORDER) / 8),
    MASK: bitMask(bitLen(FP2_ORDER)),
    ZERO: { c0: Fp7.ZERO, c1: Fp7.ZERO },
    ONE: { c0: Fp7.ONE, c1: Fp7.ZERO },
    create: (num) => num,
    isValid: ({ c0, c1 }) => typeof c0 === "bigint" && typeof c1 === "bigint",
    is0: ({ c0, c1 }) => Fp7.is0(c0) && Fp7.is0(c1),
    eql: ({ c0, c1 }, { c0: r0, c1: r1 }) => Fp7.eql(c0, r0) && Fp7.eql(c1, r1),
    neg: ({ c0, c1 }) => ({ c0: Fp7.neg(c0), c1: Fp7.neg(c1) }),
    pow: (num, power) => FpPow(Fp22, num, power),
    invertBatch: (nums) => FpInvertBatch(Fp22, nums),
    // Normalized
    add: Fp2Add,
    sub: Fp2Subtract,
    mul: Fp2Multiply,
    sqr: Fp2Square,
    // NonNormalized stuff
    addN: Fp2Add,
    subN: Fp2Subtract,
    mulN: Fp2Multiply,
    sqrN: Fp2Square,
    // Why inversion for bigint inside Fp instead of Fp2? it is even used in that context?
    div: (lhs, rhs) => Fp22.mul(lhs, typeof rhs === "bigint" ? Fp7.inv(Fp7.create(rhs)) : Fp22.inv(rhs)),
    inv: ({ c0: a, c1: b }) => {
      const factor = Fp7.inv(Fp7.create(a * a + b * b));
      return { c0: Fp7.mul(factor, Fp7.create(a)), c1: Fp7.mul(factor, Fp7.create(-b)) };
    },
    sqrt: (num) => {
      if (Fp22.eql(num, Fp22.ZERO))
        return Fp22.ZERO;
      const candidateSqrt = Fp22.pow(num, (Fp22.ORDER + _8n3) / _16n2);
      const check = Fp22.div(Fp22.sqr(candidateSqrt), num);
      const R = FP2_ROOTS_OF_UNITY;
      const divisor = [R[0], R[2], R[4], R[6]].find((r) => Fp22.eql(r, check));
      if (!divisor)
        throw new Error("No root");
      const index = R.indexOf(divisor);
      const root = R[index / 2];
      if (!root)
        throw new Error("Invalid root");
      const x1 = Fp22.div(candidateSqrt, root);
      const x2 = Fp22.neg(x1);
      const { re: re1, im: im1 } = Fp22.reim(x1);
      const { re: re2, im: im2 } = Fp22.reim(x2);
      if (im1 > im2 || im1 === im2 && re1 > re2)
        return x1;
      return x2;
    },
    // Same as sgn0_m_eq_2 in RFC 9380
    isOdd: (x) => {
      const { re: x0, im: x1 } = Fp22.reim(x);
      const sign_0 = x0 % _2n10;
      const zero_0 = x0 === _0n10;
      const sign_1 = x1 % _2n10;
      return BigInt(sign_0 || zero_0 && sign_1) == _1n11;
    },
    // Bytes util
    fromBytes(b) {
      if (b.length !== Fp22.BYTES)
        throw new Error(`fromBytes wrong length=${b.length}`);
      return { c0: Fp7.fromBytes(b.subarray(0, Fp7.BYTES)), c1: Fp7.fromBytes(b.subarray(Fp7.BYTES)) };
    },
    toBytes: ({ c0, c1 }) => concatBytes(Fp7.toBytes(c0), Fp7.toBytes(c1)),
    cmov: ({ c0, c1 }, { c0: r0, c1: r1 }, c) => ({
      c0: Fp7.cmov(c0, r0, c),
      c1: Fp7.cmov(c1, r1, c)
    }),
    // Specific utils
    // toString() {
    //   return `Fp2(${this.c0} + ${this.c1}×i)`;
    // }
    reim: ({ c0, c1 }) => ({ re: c0, im: c1 }),
    // multiply by u + 1
    mulByNonresidue: ({ c0, c1 }) => ({ c0: Fp7.sub(c0, c1), c1: Fp7.add(c0, c1) }),
    multiplyByB: ({ c0, c1 }) => {
      let t0 = Fp7.mul(c0, _4n4);
      let t1 = Fp7.mul(c1, _4n4);
      return { c0: Fp7.sub(t0, t1), c1: Fp7.add(t0, t1) };
    },
    fromBigTuple: (tuple) => {
      if (tuple.length !== 2)
        throw new Error("Invalid tuple");
      const fps = tuple.map((n) => Fp7.create(n));
      return { c0: fps[0], c1: fps[1] };
    },
    frobeniusMap: ({ c0, c1 }, power) => ({
      c0,
      c1: Fp7.mul(c1, FP2_FROBENIUS_COEFFICIENTS[power % 2])
    })
  };
  var FP2_FROBENIUS_COEFFICIENTS = [
    BigInt("0x1"),
    BigInt("0x1a0111ea397fe69a4b1ba7b6434bacd764774b84f38512bf6730d2a0f6b0f6241eabfffeb153ffffb9feffffffffaaaa")
  ].map((item) => Fp7.create(item));
  var rv1 = BigInt("0x6af0e0437ff400b6831e36d6bd17ffe48395dabc2d3435e77f76e17009241c5ee67992f72ec05f4c81084fbede3cc09");
  var FP2_ROOTS_OF_UNITY = [
    [_1n11, _0n10],
    [rv1, -rv1],
    [_0n10, _1n11],
    [rv1, rv1],
    [-_1n11, _0n10],
    [-rv1, rv1],
    [_0n10, -_1n11],
    [-rv1, -rv1]
  ].map((pair) => Fp22.fromBigTuple(pair));
  var Fp6Add = ({ c0, c1, c2 }, { c0: r0, c1: r1, c2: r2 }) => ({
    c0: Fp22.add(c0, r0),
    c1: Fp22.add(c1, r1),
    c2: Fp22.add(c2, r2)
  });
  var Fp6Subtract = ({ c0, c1, c2 }, { c0: r0, c1: r1, c2: r2 }) => ({
    c0: Fp22.sub(c0, r0),
    c1: Fp22.sub(c1, r1),
    c2: Fp22.sub(c2, r2)
  });
  var Fp6Multiply = ({ c0, c1, c2 }, rhs) => {
    if (typeof rhs === "bigint") {
      return {
        c0: Fp22.mul(c0, rhs),
        c1: Fp22.mul(c1, rhs),
        c2: Fp22.mul(c2, rhs)
      };
    }
    const { c0: r0, c1: r1, c2: r2 } = rhs;
    const t0 = Fp22.mul(c0, r0);
    const t1 = Fp22.mul(c1, r1);
    const t2 = Fp22.mul(c2, r2);
    return {
      // t0 + (c1 + c2) * (r1 * r2) - (T1 + T2) * (u + 1)
      c0: Fp22.add(t0, Fp22.mulByNonresidue(Fp22.sub(Fp22.mul(Fp22.add(c1, c2), Fp22.add(r1, r2)), Fp22.add(t1, t2)))),
      // (c0 + c1) * (r0 + r1) - (T0 + T1) + T2 * (u + 1)
      c1: Fp22.add(Fp22.sub(Fp22.mul(Fp22.add(c0, c1), Fp22.add(r0, r1)), Fp22.add(t0, t1)), Fp22.mulByNonresidue(t2)),
      // T1 + (c0 + c2) * (r0 + r2) - T0 + T2
      c2: Fp22.sub(Fp22.add(t1, Fp22.mul(Fp22.add(c0, c2), Fp22.add(r0, r2))), Fp22.add(t0, t2))
    };
  };
  var Fp6Square = ({ c0, c1, c2 }) => {
    let t0 = Fp22.sqr(c0);
    let t1 = Fp22.mul(Fp22.mul(c0, c1), _2n10);
    let t3 = Fp22.mul(Fp22.mul(c1, c2), _2n10);
    let t4 = Fp22.sqr(c2);
    return {
      c0: Fp22.add(Fp22.mulByNonresidue(t3), t0),
      // T3 * (u + 1) + T0
      c1: Fp22.add(Fp22.mulByNonresidue(t4), t1),
      // T4 * (u + 1) + T1
      // T1 + (c0 - c1 + c2)² + T3 - T0 - T4
      c2: Fp22.sub(Fp22.sub(Fp22.add(Fp22.add(t1, Fp22.sqr(Fp22.add(Fp22.sub(c0, c1), c2))), t3), t0), t4)
    };
  };
  var Fp62 = {
    ORDER: Fp22.ORDER,
    // TODO: unused, but need to verify
    BITS: 3 * Fp22.BITS,
    BYTES: 3 * Fp22.BYTES,
    MASK: bitMask(3 * Fp22.BITS),
    ZERO: { c0: Fp22.ZERO, c1: Fp22.ZERO, c2: Fp22.ZERO },
    ONE: { c0: Fp22.ONE, c1: Fp22.ZERO, c2: Fp22.ZERO },
    create: (num) => num,
    isValid: ({ c0, c1, c2 }) => Fp22.isValid(c0) && Fp22.isValid(c1) && Fp22.isValid(c2),
    is0: ({ c0, c1, c2 }) => Fp22.is0(c0) && Fp22.is0(c1) && Fp22.is0(c2),
    neg: ({ c0, c1, c2 }) => ({ c0: Fp22.neg(c0), c1: Fp22.neg(c1), c2: Fp22.neg(c2) }),
    eql: ({ c0, c1, c2 }, { c0: r0, c1: r1, c2: r2 }) => Fp22.eql(c0, r0) && Fp22.eql(c1, r1) && Fp22.eql(c2, r2),
    sqrt: () => {
      throw new Error("Not implemented");
    },
    // Do we need division by bigint at all? Should be done via order:
    div: (lhs, rhs) => Fp62.mul(lhs, typeof rhs === "bigint" ? Fp7.inv(Fp7.create(rhs)) : Fp62.inv(rhs)),
    pow: (num, power) => FpPow(Fp62, num, power),
    invertBatch: (nums) => FpInvertBatch(Fp62, nums),
    // Normalized
    add: Fp6Add,
    sub: Fp6Subtract,
    mul: Fp6Multiply,
    sqr: Fp6Square,
    // NonNormalized stuff
    addN: Fp6Add,
    subN: Fp6Subtract,
    mulN: Fp6Multiply,
    sqrN: Fp6Square,
    inv: ({ c0, c1, c2 }) => {
      let t0 = Fp22.sub(Fp22.sqr(c0), Fp22.mulByNonresidue(Fp22.mul(c2, c1)));
      let t1 = Fp22.sub(Fp22.mulByNonresidue(Fp22.sqr(c2)), Fp22.mul(c0, c1));
      let t2 = Fp22.sub(Fp22.sqr(c1), Fp22.mul(c0, c2));
      let t4 = Fp22.inv(Fp22.add(Fp22.mulByNonresidue(Fp22.add(Fp22.mul(c2, t1), Fp22.mul(c1, t2))), Fp22.mul(c0, t0)));
      return { c0: Fp22.mul(t4, t0), c1: Fp22.mul(t4, t1), c2: Fp22.mul(t4, t2) };
    },
    // Bytes utils
    fromBytes: (b) => {
      if (b.length !== Fp62.BYTES)
        throw new Error(`fromBytes wrong length=${b.length}`);
      return {
        c0: Fp22.fromBytes(b.subarray(0, Fp22.BYTES)),
        c1: Fp22.fromBytes(b.subarray(Fp22.BYTES, 2 * Fp22.BYTES)),
        c2: Fp22.fromBytes(b.subarray(2 * Fp22.BYTES))
      };
    },
    toBytes: ({ c0, c1, c2 }) => concatBytes(Fp22.toBytes(c0), Fp22.toBytes(c1), Fp22.toBytes(c2)),
    cmov: ({ c0, c1, c2 }, { c0: r0, c1: r1, c2: r2 }, c) => ({
      c0: Fp22.cmov(c0, r0, c),
      c1: Fp22.cmov(c1, r1, c),
      c2: Fp22.cmov(c2, r2, c)
    }),
    // Utils
    //   fromTriple(triple: [Fp2, Fp2, Fp2]) {
    //     return new Fp6(...triple);
    //   }
    //   toString() {
    //     return `Fp6(${this.c0} + ${this.c1} * v, ${this.c2} * v^2)`;
    //   }
    fromBigSix: (t) => {
      if (!Array.isArray(t) || t.length !== 6)
        throw new Error("Invalid Fp6 usage");
      return {
        c0: Fp22.fromBigTuple(t.slice(0, 2)),
        c1: Fp22.fromBigTuple(t.slice(2, 4)),
        c2: Fp22.fromBigTuple(t.slice(4, 6))
      };
    },
    frobeniusMap: ({ c0, c1, c2 }, power) => ({
      c0: Fp22.frobeniusMap(c0, power),
      c1: Fp22.mul(Fp22.frobeniusMap(c1, power), FP6_FROBENIUS_COEFFICIENTS_1[power % 6]),
      c2: Fp22.mul(Fp22.frobeniusMap(c2, power), FP6_FROBENIUS_COEFFICIENTS_2[power % 6])
    }),
    mulByNonresidue: ({ c0, c1, c2 }) => ({ c0: Fp22.mulByNonresidue(c2), c1: c0, c2: c1 }),
    // Sparse multiplication
    multiplyBy1: ({ c0, c1, c2 }, b1) => ({
      c0: Fp22.mulByNonresidue(Fp22.mul(c2, b1)),
      c1: Fp22.mul(c0, b1),
      c2: Fp22.mul(c1, b1)
    }),
    // Sparse multiplication
    multiplyBy01({ c0, c1, c2 }, b0, b1) {
      let t0 = Fp22.mul(c0, b0);
      let t1 = Fp22.mul(c1, b1);
      return {
        // ((c1 + c2) * b1 - T1) * (u + 1) + T0
        c0: Fp22.add(Fp22.mulByNonresidue(Fp22.sub(Fp22.mul(Fp22.add(c1, c2), b1), t1)), t0),
        // (b0 + b1) * (c0 + c1) - T0 - T1
        c1: Fp22.sub(Fp22.sub(Fp22.mul(Fp22.add(b0, b1), Fp22.add(c0, c1)), t0), t1),
        // (c0 + c2) * b0 - T0 + T1
        c2: Fp22.add(Fp22.sub(Fp22.mul(Fp22.add(c0, c2), b0), t0), t1)
      };
    },
    multiplyByFp2: ({ c0, c1, c2 }, rhs) => ({
      c0: Fp22.mul(c0, rhs),
      c1: Fp22.mul(c1, rhs),
      c2: Fp22.mul(c2, rhs)
    })
  };
  var FP6_FROBENIUS_COEFFICIENTS_1 = [
    [BigInt("0x1"), BigInt("0x0")],
    [
      BigInt("0x0"),
      BigInt("0x1a0111ea397fe699ec02408663d4de85aa0d857d89759ad4897d29650fb85f9b409427eb4f49fffd8bfd00000000aaac")
    ],
    [
      BigInt("0x00000000000000005f19672fdf76ce51ba69c6076a0f77eaddb3a93be6f89688de17d813620a00022e01fffffffefffe"),
      BigInt("0x0")
    ],
    [BigInt("0x0"), BigInt("0x1")],
    [
      BigInt("0x1a0111ea397fe699ec02408663d4de85aa0d857d89759ad4897d29650fb85f9b409427eb4f49fffd8bfd00000000aaac"),
      BigInt("0x0")
    ],
    [
      BigInt("0x0"),
      BigInt("0x00000000000000005f19672fdf76ce51ba69c6076a0f77eaddb3a93be6f89688de17d813620a00022e01fffffffefffe")
    ]
  ].map((pair) => Fp22.fromBigTuple(pair));
  var FP6_FROBENIUS_COEFFICIENTS_2 = [
    [BigInt("0x1"), BigInt("0x0")],
    [
      BigInt("0x1a0111ea397fe699ec02408663d4de85aa0d857d89759ad4897d29650fb85f9b409427eb4f49fffd8bfd00000000aaad"),
      BigInt("0x0")
    ],
    [
      BigInt("0x1a0111ea397fe699ec02408663d4de85aa0d857d89759ad4897d29650fb85f9b409427eb4f49fffd8bfd00000000aaac"),
      BigInt("0x0")
    ],
    [
      BigInt("0x1a0111ea397fe69a4b1ba7b6434bacd764774b84f38512bf6730d2a0f6b0f6241eabfffeb153ffffb9feffffffffaaaa"),
      BigInt("0x0")
    ],
    [
      BigInt("0x00000000000000005f19672fdf76ce51ba69c6076a0f77eaddb3a93be6f89688de17d813620a00022e01fffffffefffe"),
      BigInt("0x0")
    ],
    [
      BigInt("0x00000000000000005f19672fdf76ce51ba69c6076a0f77eaddb3a93be6f89688de17d813620a00022e01fffffffeffff"),
      BigInt("0x0")
    ]
  ].map((pair) => Fp22.fromBigTuple(pair));
  var BLS_X = BigInt("0xd201000000010000");
  var BLS_X_LEN = bitLen(BLS_X);
  var Fp12Add = ({ c0, c1 }, { c0: r0, c1: r1 }) => ({
    c0: Fp62.add(c0, r0),
    c1: Fp62.add(c1, r1)
  });
  var Fp12Subtract = ({ c0, c1 }, { c0: r0, c1: r1 }) => ({
    c0: Fp62.sub(c0, r0),
    c1: Fp62.sub(c1, r1)
  });
  var Fp12Multiply = ({ c0, c1 }, rhs) => {
    if (typeof rhs === "bigint")
      return { c0: Fp62.mul(c0, rhs), c1: Fp62.mul(c1, rhs) };
    let { c0: r0, c1: r1 } = rhs;
    let t1 = Fp62.mul(c0, r0);
    let t2 = Fp62.mul(c1, r1);
    return {
      c0: Fp62.add(t1, Fp62.mulByNonresidue(t2)),
      // T1 + T2 * v
      // (c0 + c1) * (r0 + r1) - (T1 + T2)
      c1: Fp62.sub(Fp62.mul(Fp62.add(c0, c1), Fp62.add(r0, r1)), Fp62.add(t1, t2))
    };
  };
  var Fp12Square = ({ c0, c1 }) => {
    let ab = Fp62.mul(c0, c1);
    return {
      // (c1 * v + c0) * (c0 + c1) - AB - AB * v
      c0: Fp62.sub(Fp62.sub(Fp62.mul(Fp62.add(Fp62.mulByNonresidue(c1), c0), Fp62.add(c0, c1)), ab), Fp62.mulByNonresidue(ab)),
      c1: Fp62.add(ab, ab)
    };
  };
  function Fp4Square(a, b) {
    const a2 = Fp22.sqr(a);
    const b2 = Fp22.sqr(b);
    return {
      first: Fp22.add(Fp22.mulByNonresidue(b2), a2),
      // b² * Nonresidue + a²
      second: Fp22.sub(Fp22.sub(Fp22.sqr(Fp22.add(a, b)), a2), b2)
      // (a + b)² - a² - b²
    };
  }
  var Fp12 = {
    ORDER: Fp22.ORDER,
    // TODO: unused, but need to verify
    BITS: 2 * Fp22.BITS,
    BYTES: 2 * Fp22.BYTES,
    MASK: bitMask(2 * Fp22.BITS),
    ZERO: { c0: Fp62.ZERO, c1: Fp62.ZERO },
    ONE: { c0: Fp62.ONE, c1: Fp62.ZERO },
    create: (num) => num,
    isValid: ({ c0, c1 }) => Fp62.isValid(c0) && Fp62.isValid(c1),
    is0: ({ c0, c1 }) => Fp62.is0(c0) && Fp62.is0(c1),
    neg: ({ c0, c1 }) => ({ c0: Fp62.neg(c0), c1: Fp62.neg(c1) }),
    eql: ({ c0, c1 }, { c0: r0, c1: r1 }) => Fp62.eql(c0, r0) && Fp62.eql(c1, r1),
    sqrt: () => {
      throw new Error("Not implemented");
    },
    inv: ({ c0, c1 }) => {
      let t = Fp62.inv(Fp62.sub(Fp62.sqr(c0), Fp62.mulByNonresidue(Fp62.sqr(c1))));
      return { c0: Fp62.mul(c0, t), c1: Fp62.neg(Fp62.mul(c1, t)) };
    },
    div: (lhs, rhs) => Fp12.mul(lhs, typeof rhs === "bigint" ? Fp7.inv(Fp7.create(rhs)) : Fp12.inv(rhs)),
    pow: (num, power) => FpPow(Fp12, num, power),
    invertBatch: (nums) => FpInvertBatch(Fp12, nums),
    // Normalized
    add: Fp12Add,
    sub: Fp12Subtract,
    mul: Fp12Multiply,
    sqr: Fp12Square,
    // NonNormalized stuff
    addN: Fp12Add,
    subN: Fp12Subtract,
    mulN: Fp12Multiply,
    sqrN: Fp12Square,
    // Bytes utils
    fromBytes: (b) => {
      if (b.length !== Fp12.BYTES)
        throw new Error(`fromBytes wrong length=${b.length}`);
      return {
        c0: Fp62.fromBytes(b.subarray(0, Fp62.BYTES)),
        c1: Fp62.fromBytes(b.subarray(Fp62.BYTES))
      };
    },
    toBytes: ({ c0, c1 }) => concatBytes(Fp62.toBytes(c0), Fp62.toBytes(c1)),
    cmov: ({ c0, c1 }, { c0: r0, c1: r1 }, c) => ({
      c0: Fp62.cmov(c0, r0, c),
      c1: Fp62.cmov(c1, r1, c)
    }),
    // Utils
    // toString() {
    //   return `Fp12(${this.c0} + ${this.c1} * w)`;
    // },
    // fromTuple(c: [Fp6, Fp6]) {
    //   return new Fp12(...c);
    // }
    fromBigTwelve: (t) => ({
      c0: Fp62.fromBigSix(t.slice(0, 6)),
      c1: Fp62.fromBigSix(t.slice(6, 12))
    }),
    // Raises to q**i -th power
    frobeniusMap(lhs, power) {
      const r0 = Fp62.frobeniusMap(lhs.c0, power);
      const { c0, c1, c2 } = Fp62.frobeniusMap(lhs.c1, power);
      const coeff = FP12_FROBENIUS_COEFFICIENTS[power % 12];
      return {
        c0: r0,
        c1: Fp62.create({
          c0: Fp22.mul(c0, coeff),
          c1: Fp22.mul(c1, coeff),
          c2: Fp22.mul(c2, coeff)
        })
      };
    },
    // Sparse multiplication
    multiplyBy014: ({ c0, c1 }, o0, o1, o4) => {
      let t0 = Fp62.multiplyBy01(c0, o0, o1);
      let t1 = Fp62.multiplyBy1(c1, o4);
      return {
        c0: Fp62.add(Fp62.mulByNonresidue(t1), t0),
        // T1 * v + T0
        // (c1 + c0) * [o0, o1+o4] - T0 - T1
        c1: Fp62.sub(Fp62.sub(Fp62.multiplyBy01(Fp62.add(c1, c0), o0, Fp22.add(o1, o4)), t0), t1)
      };
    },
    multiplyByFp2: ({ c0, c1 }, rhs) => ({
      c0: Fp62.multiplyByFp2(c0, rhs),
      c1: Fp62.multiplyByFp2(c1, rhs)
    }),
    conjugate: ({ c0, c1 }) => ({ c0, c1: Fp62.neg(c1) }),
    // A cyclotomic group is a subgroup of Fp^n defined by
    //   GΦₙ(p) = {α ∈ Fpⁿ : α^Φₙ(p) = 1}
    // The result of any pairing is in a cyclotomic subgroup
    // https://eprint.iacr.org/2009/565.pdf
    _cyclotomicSquare: ({ c0, c1 }) => {
      const { c0: c0c0, c1: c0c1, c2: c0c2 } = c0;
      const { c0: c1c0, c1: c1c1, c2: c1c2 } = c1;
      const { first: t3, second: t4 } = Fp4Square(c0c0, c1c1);
      const { first: t5, second: t6 } = Fp4Square(c1c0, c0c2);
      const { first: t7, second: t8 } = Fp4Square(c0c1, c1c2);
      let t9 = Fp22.mulByNonresidue(t8);
      return {
        c0: Fp62.create({
          c0: Fp22.add(Fp22.mul(Fp22.sub(t3, c0c0), _2n10), t3),
          // 2 * (T3 - c0c0)  + T3
          c1: Fp22.add(Fp22.mul(Fp22.sub(t5, c0c1), _2n10), t5),
          // 2 * (T5 - c0c1)  + T5
          c2: Fp22.add(Fp22.mul(Fp22.sub(t7, c0c2), _2n10), t7)
        }),
        // 2 * (T7 - c0c2)  + T7
        c1: Fp62.create({
          c0: Fp22.add(Fp22.mul(Fp22.add(t9, c1c0), _2n10), t9),
          // 2 * (T9 + c1c0) + T9
          c1: Fp22.add(Fp22.mul(Fp22.add(t4, c1c1), _2n10), t4),
          // 2 * (T4 + c1c1) + T4
          c2: Fp22.add(Fp22.mul(Fp22.add(t6, c1c2), _2n10), t6)
        })
      };
    },
    _cyclotomicExp(num, n) {
      let z = Fp12.ONE;
      for (let i = BLS_X_LEN - 1; i >= 0; i--) {
        z = Fp12._cyclotomicSquare(z);
        if (bitGet(n, i))
          z = Fp12.mul(z, num);
      }
      return z;
    },
    // https://eprint.iacr.org/2010/354.pdf
    // https://eprint.iacr.org/2009/565.pdf
    finalExponentiate: (num) => {
      const x = BLS_X;
      const t0 = Fp12.div(Fp12.frobeniusMap(num, 6), num);
      const t1 = Fp12.mul(Fp12.frobeniusMap(t0, 2), t0);
      const t2 = Fp12.conjugate(Fp12._cyclotomicExp(t1, x));
      const t3 = Fp12.mul(Fp12.conjugate(Fp12._cyclotomicSquare(t1)), t2);
      const t4 = Fp12.conjugate(Fp12._cyclotomicExp(t3, x));
      const t5 = Fp12.conjugate(Fp12._cyclotomicExp(t4, x));
      const t6 = Fp12.mul(Fp12.conjugate(Fp12._cyclotomicExp(t5, x)), Fp12._cyclotomicSquare(t2));
      const t7 = Fp12.conjugate(Fp12._cyclotomicExp(t6, x));
      const t2_t5_pow_q2 = Fp12.frobeniusMap(Fp12.mul(t2, t5), 2);
      const t4_t1_pow_q3 = Fp12.frobeniusMap(Fp12.mul(t4, t1), 3);
      const t6_t1c_pow_q1 = Fp12.frobeniusMap(Fp12.mul(t6, Fp12.conjugate(t1)), 1);
      const t7_t3c_t1 = Fp12.mul(Fp12.mul(t7, Fp12.conjugate(t3)), t1);
      return Fp12.mul(Fp12.mul(Fp12.mul(t2_t5_pow_q2, t4_t1_pow_q3), t6_t1c_pow_q1), t7_t3c_t1);
    }
  };
  var FP12_FROBENIUS_COEFFICIENTS = [
    [BigInt("0x1"), BigInt("0x0")],
    [
      BigInt("0x1904d3bf02bb0667c231beb4202c0d1f0fd603fd3cbd5f4f7b2443d784bab9c4f67ea53d63e7813d8d0775ed92235fb8"),
      BigInt("0x00fc3e2b36c4e03288e9e902231f9fb854a14787b6c7b36fec0c8ec971f63c5f282d5ac14d6c7ec22cf78a126ddc4af3")
    ],
    [
      BigInt("0x00000000000000005f19672fdf76ce51ba69c6076a0f77eaddb3a93be6f89688de17d813620a00022e01fffffffeffff"),
      BigInt("0x0")
    ],
    [
      BigInt("0x135203e60180a68ee2e9c448d77a2cd91c3dedd930b1cf60ef396489f61eb45e304466cf3e67fa0af1ee7b04121bdea2"),
      BigInt("0x06af0e0437ff400b6831e36d6bd17ffe48395dabc2d3435e77f76e17009241c5ee67992f72ec05f4c81084fbede3cc09")
    ],
    [
      BigInt("0x00000000000000005f19672fdf76ce51ba69c6076a0f77eaddb3a93be6f89688de17d813620a00022e01fffffffefffe"),
      BigInt("0x0")
    ],
    [
      BigInt("0x144e4211384586c16bd3ad4afa99cc9170df3560e77982d0db45f3536814f0bd5871c1908bd478cd1ee605167ff82995"),
      BigInt("0x05b2cfd9013a5fd8df47fa6b48b1e045f39816240c0b8fee8beadf4d8e9c0566c63a3e6e257f87329b18fae980078116")
    ],
    [
      BigInt("0x1a0111ea397fe69a4b1ba7b6434bacd764774b84f38512bf6730d2a0f6b0f6241eabfffeb153ffffb9feffffffffaaaa"),
      BigInt("0x0")
    ],
    [
      BigInt("0x00fc3e2b36c4e03288e9e902231f9fb854a14787b6c7b36fec0c8ec971f63c5f282d5ac14d6c7ec22cf78a126ddc4af3"),
      BigInt("0x1904d3bf02bb0667c231beb4202c0d1f0fd603fd3cbd5f4f7b2443d784bab9c4f67ea53d63e7813d8d0775ed92235fb8")
    ],
    [
      BigInt("0x1a0111ea397fe699ec02408663d4de85aa0d857d89759ad4897d29650fb85f9b409427eb4f49fffd8bfd00000000aaac"),
      BigInt("0x0")
    ],
    [
      BigInt("0x06af0e0437ff400b6831e36d6bd17ffe48395dabc2d3435e77f76e17009241c5ee67992f72ec05f4c81084fbede3cc09"),
      BigInt("0x135203e60180a68ee2e9c448d77a2cd91c3dedd930b1cf60ef396489f61eb45e304466cf3e67fa0af1ee7b04121bdea2")
    ],
    [
      BigInt("0x1a0111ea397fe699ec02408663d4de85aa0d857d89759ad4897d29650fb85f9b409427eb4f49fffd8bfd00000000aaad"),
      BigInt("0x0")
    ],
    [
      BigInt("0x05b2cfd9013a5fd8df47fa6b48b1e045f39816240c0b8fee8beadf4d8e9c0566c63a3e6e257f87329b18fae980078116"),
      BigInt("0x144e4211384586c16bd3ad4afa99cc9170df3560e77982d0db45f3536814f0bd5871c1908bd478cd1ee605167ff82995")
    ]
  ].map((n) => Fp22.fromBigTuple(n));
  var isogenyMapG2 = isogenyMap(Fp22, [
    // xNum
    [
      [
        "0x5c759507e8e333ebb5b7a9a47d7ed8532c52d39fd3a042a88b58423c50ae15d5c2638e343d9c71c6238aaaaaaaa97d6",
        "0x5c759507e8e333ebb5b7a9a47d7ed8532c52d39fd3a042a88b58423c50ae15d5c2638e343d9c71c6238aaaaaaaa97d6"
      ],
      [
        "0x0",
        "0x11560bf17baa99bc32126fced787c88f984f87adf7ae0c7f9a208c6b4f20a4181472aaa9cb8d555526a9ffffffffc71a"
      ],
      [
        "0x11560bf17baa99bc32126fced787c88f984f87adf7ae0c7f9a208c6b4f20a4181472aaa9cb8d555526a9ffffffffc71e",
        "0x8ab05f8bdd54cde190937e76bc3e447cc27c3d6fbd7063fcd104635a790520c0a395554e5c6aaaa9354ffffffffe38d"
      ],
      [
        "0x171d6541fa38ccfaed6dea691f5fb614cb14b4e7f4e810aa22d6108f142b85757098e38d0f671c7188e2aaaaaaaa5ed1",
        "0x0"
      ]
    ],
    // xDen
    [
      [
        "0x0",
        "0x1a0111ea397fe69a4b1ba7b6434bacd764774b84f38512bf6730d2a0f6b0f6241eabfffeb153ffffb9feffffffffaa63"
      ],
      [
        "0xc",
        "0x1a0111ea397fe69a4b1ba7b6434bacd764774b84f38512bf6730d2a0f6b0f6241eabfffeb153ffffb9feffffffffaa9f"
      ],
      ["0x1", "0x0"]
      // LAST 1
    ],
    // yNum
    [
      [
        "0x1530477c7ab4113b59a4c18b076d11930f7da5d4a07f649bf54439d87d27e500fc8c25ebf8c92f6812cfc71c71c6d706",
        "0x1530477c7ab4113b59a4c18b076d11930f7da5d4a07f649bf54439d87d27e500fc8c25ebf8c92f6812cfc71c71c6d706"
      ],
      [
        "0x0",
        "0x5c759507e8e333ebb5b7a9a47d7ed8532c52d39fd3a042a88b58423c50ae15d5c2638e343d9c71c6238aaaaaaaa97be"
      ],
      [
        "0x11560bf17baa99bc32126fced787c88f984f87adf7ae0c7f9a208c6b4f20a4181472aaa9cb8d555526a9ffffffffc71c",
        "0x8ab05f8bdd54cde190937e76bc3e447cc27c3d6fbd7063fcd104635a790520c0a395554e5c6aaaa9354ffffffffe38f"
      ],
      [
        "0x124c9ad43b6cf79bfbf7043de3811ad0761b0f37a1e26286b0e977c69aa274524e79097a56dc4bd9e1b371c71c718b10",
        "0x0"
      ]
    ],
    // yDen
    [
      [
        "0x1a0111ea397fe69a4b1ba7b6434bacd764774b84f38512bf6730d2a0f6b0f6241eabfffeb153ffffb9feffffffffa8fb",
        "0x1a0111ea397fe69a4b1ba7b6434bacd764774b84f38512bf6730d2a0f6b0f6241eabfffeb153ffffb9feffffffffa8fb"
      ],
      [
        "0x0",
        "0x1a0111ea397fe69a4b1ba7b6434bacd764774b84f38512bf6730d2a0f6b0f6241eabfffeb153ffffb9feffffffffa9d3"
      ],
      [
        "0x12",
        "0x1a0111ea397fe69a4b1ba7b6434bacd764774b84f38512bf6730d2a0f6b0f6241eabfffeb153ffffb9feffffffffaa99"
      ],
      ["0x1", "0x0"]
      // LAST 1
    ]
  ].map((i) => i.map((pair) => Fp22.fromBigTuple(pair.map(BigInt)))));
  var isogenyMapG1 = isogenyMap(Fp7, [
    // xNum
    [
      "0x11a05f2b1e833340b809101dd99815856b303e88a2d7005ff2627b56cdb4e2c85610c2d5f2e62d6eaeac1662734649b7",
      "0x17294ed3e943ab2f0588bab22147a81c7c17e75b2f6a8417f565e33c70d1e86b4838f2a6f318c356e834eef1b3cb83bb",
      "0xd54005db97678ec1d1048c5d10a9a1bce032473295983e56878e501ec68e25c958c3e3d2a09729fe0179f9dac9edcb0",
      "0x1778e7166fcc6db74e0609d307e55412d7f5e4656a8dbf25f1b33289f1b330835336e25ce3107193c5b388641d9b6861",
      "0xe99726a3199f4436642b4b3e4118e5499db995a1257fb3f086eeb65982fac18985a286f301e77c451154ce9ac8895d9",
      "0x1630c3250d7313ff01d1201bf7a74ab5db3cb17dd952799b9ed3ab9097e68f90a0870d2dcae73d19cd13c1c66f652983",
      "0xd6ed6553fe44d296a3726c38ae652bfb11586264f0f8ce19008e218f9c86b2a8da25128c1052ecaddd7f225a139ed84",
      "0x17b81e7701abdbe2e8743884d1117e53356de5ab275b4db1a682c62ef0f2753339b7c8f8c8f475af9ccb5618e3f0c88e",
      "0x80d3cf1f9a78fc47b90b33563be990dc43b756ce79f5574a2c596c928c5d1de4fa295f296b74e956d71986a8497e317",
      "0x169b1f8e1bcfa7c42e0c37515d138f22dd2ecb803a0c5c99676314baf4bb1b7fa3190b2edc0327797f241067be390c9e",
      "0x10321da079ce07e272d8ec09d2565b0dfa7dccdde6787f96d50af36003b14866f69b771f8c285decca67df3f1605fb7b",
      "0x6e08c248e260e70bd1e962381edee3d31d79d7e22c837bc23c0bf1bc24c6b68c24b1b80b64d391fa9c8ba2e8ba2d229"
    ],
    // xDen
    [
      "0x8ca8d548cff19ae18b2e62f4bd3fa6f01d5ef4ba35b48ba9c9588617fc8ac62b558d681be343df8993cf9fa40d21b1c",
      "0x12561a5deb559c4348b4711298e536367041e8ca0cf0800c0126c2588c48bf5713daa8846cb026e9e5c8276ec82b3bff",
      "0xb2962fe57a3225e8137e629bff2991f6f89416f5a718cd1fca64e00b11aceacd6a3d0967c94fedcfcc239ba5cb83e19",
      "0x3425581a58ae2fec83aafef7c40eb545b08243f16b1655154cca8abc28d6fd04976d5243eecf5c4130de8938dc62cd8",
      "0x13a8e162022914a80a6f1d5f43e7a07dffdfc759a12062bb8d6b44e833b306da9bd29ba81f35781d539d395b3532a21e",
      "0xe7355f8e4e667b955390f7f0506c6e9395735e9ce9cad4d0a43bcef24b8982f7400d24bc4228f11c02df9a29f6304a5",
      "0x772caacf16936190f3e0c63e0596721570f5799af53a1894e2e073062aede9cea73b3538f0de06cec2574496ee84a3a",
      "0x14a7ac2a9d64a8b230b3f5b074cf01996e7f63c21bca68a81996e1cdf9822c580fa5b9489d11e2d311f7d99bbdcc5a5e",
      "0xa10ecf6ada54f825e920b3dafc7a3cce07f8d1d7161366b74100da67f39883503826692abba43704776ec3a79a1d641",
      "0x95fc13ab9e92ad4476d6e3eb3a56680f682b4ee96f7d03776df533978f31c1593174e4b4b7865002d6384d168ecdd0a",
      "0x000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001"
      // LAST 1
    ],
    // yNum
    [
      "0x90d97c81ba24ee0259d1f094980dcfa11ad138e48a869522b52af6c956543d3cd0c7aee9b3ba3c2be9845719707bb33",
      "0x134996a104ee5811d51036d776fb46831223e96c254f383d0f906343eb67ad34d6c56711962fa8bfe097e75a2e41c696",
      "0xcc786baa966e66f4a384c86a3b49942552e2d658a31ce2c344be4b91400da7d26d521628b00523b8dfe240c72de1f6",
      "0x1f86376e8981c217898751ad8746757d42aa7b90eeb791c09e4a3ec03251cf9de405aba9ec61deca6355c77b0e5f4cb",
      "0x8cc03fdefe0ff135caf4fe2a21529c4195536fbe3ce50b879833fd221351adc2ee7f8dc099040a841b6daecf2e8fedb",
      "0x16603fca40634b6a2211e11db8f0a6a074a7d0d4afadb7bd76505c3d3ad5544e203f6326c95a807299b23ab13633a5f0",
      "0x4ab0b9bcfac1bbcb2c977d027796b3ce75bb8ca2be184cb5231413c4d634f3747a87ac2460f415ec961f8855fe9d6f2",
      "0x987c8d5333ab86fde9926bd2ca6c674170a05bfe3bdd81ffd038da6c26c842642f64550fedfe935a15e4ca31870fb29",
      "0x9fc4018bd96684be88c9e221e4da1bb8f3abd16679dc26c1e8b6e6a1f20cabe69d65201c78607a360370e577bdba587",
      "0xe1bba7a1186bdb5223abde7ada14a23c42a0ca7915af6fe06985e7ed1e4d43b9b3f7055dd4eba6f2bafaaebca731c30",
      "0x19713e47937cd1be0dfd0b8f1d43fb93cd2fcbcb6caf493fd1183e416389e61031bf3a5cce3fbafce813711ad011c132",
      "0x18b46a908f36f6deb918c143fed2edcc523559b8aaf0c2462e6bfe7f911f643249d9cdf41b44d606ce07c8a4d0074d8e",
      "0xb182cac101b9399d155096004f53f447aa7b12a3426b08ec02710e807b4633f06c851c1919211f20d4c04f00b971ef8",
      "0x245a394ad1eca9b72fc00ae7be315dc757b3b080d4c158013e6632d3c40659cc6cf90ad1c232a6442d9d3f5db980133",
      "0x5c129645e44cf1102a159f748c4a3fc5e673d81d7e86568d9ab0f5d396a7ce46ba1049b6579afb7866b1e715475224b",
      "0x15e6be4e990f03ce4ea50b3b42df2eb5cb181d8f84965a3957add4fa95af01b2b665027efec01c7704b456be69c8b604"
    ],
    // yDen
    [
      "0x16112c4c3a9c98b252181140fad0eae9601a6de578980be6eec3232b5be72e7a07f3688ef60c206d01479253b03663c1",
      "0x1962d75c2381201e1a0cbd6c43c348b885c84ff731c4d59ca4a10356f453e01f78a4260763529e3532f6102c2e49a03d",
      "0x58df3306640da276faaae7d6e8eb15778c4855551ae7f310c35a5dd279cd2eca6757cd636f96f891e2538b53dbf67f2",
      "0x16b7d288798e5395f20d23bf89edb4d1d115c5dbddbcd30e123da489e726af41727364f2c28297ada8d26d98445f5416",
      "0xbe0e079545f43e4b00cc912f8228ddcc6d19c9f0f69bbb0542eda0fc9dec916a20b15dc0fd2ededda39142311a5001d",
      "0x8d9e5297186db2d9fb266eaac783182b70152c65550d881c5ecd87b6f0f5a6449f38db9dfa9cce202c6477faaf9b7ac",
      "0x166007c08a99db2fc3ba8734ace9824b5eecfdfa8d0cf8ef5dd365bc400a0051d5fa9c01a58b1fb93d1a1399126a775c",
      "0x16a3ef08be3ea7ea03bcddfabba6ff6ee5a4375efa1f4fd7feb34fd206357132b920f5b00801dee460ee415a15812ed9",
      "0x1866c8ed336c61231a1be54fd1d74cc4f9fb0ce4c6af5920abc5750c4bf39b4852cfe2f7bb9248836b233d9d55535d4a",
      "0x167a55cda70a6e1cea820597d94a84903216f763e13d87bb5308592e7ea7d4fbc7385ea3d529b35e346ef48bb8913f55",
      "0x4d2f259eea405bd48f010a01ad2911d9c6dd039bb61a6290e591b36e636a5c871a5c29f4f83060400f8b49cba8f6aa8",
      "0xaccbb67481d033ff5852c1e48c50c477f94ff8aefce42d28c0f9a88cea7913516f968986f7ebbea9684b529e2561092",
      "0xad6b9514c767fe3c3613144b45f1496543346d98adf02267d5ceef9a00d9b8693000763e3b90ac11e99b138573345cc",
      "0x2660400eb2e4f3b628bdd0d53cd76f2bf565b94e72927c1cb748df27942480e420517bd8714cc80d1fadc1326ed06f7",
      "0xe0fa1d816ddc03e6b24255e0d7819c171c40f65e273b853324efcd6356caa205ca2f570f13497804415473a1d634b8f",
      "0x000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001"
      // LAST 1
    ]
  ].map((i) => i.map((j) => BigInt(j))));
  var G2_SWU = mapToCurveSimpleSWU(Fp22, {
    A: Fp22.create({ c0: Fp7.create(_0n10), c1: Fp7.create(BigInt(240)) }),
    // A' = 240 * I
    B: Fp22.create({ c0: Fp7.create(BigInt(1012)), c1: Fp7.create(BigInt(1012)) }),
    // B' = 1012 * (1 + I)
    Z: Fp22.create({ c0: Fp7.create(BigInt(-2)), c1: Fp7.create(BigInt(-1)) })
    // Z: -(2 + I)
  });
  var G1_SWU = mapToCurveSimpleSWU(Fp7, {
    A: Fp7.create(BigInt("0x144698a3b8e9433d693a02c96d4982b0ea985383ee66a8d8e8981aefd881ac98936f8da0e0f97f5cf428082d584c1d")),
    B: Fp7.create(BigInt("0x12e2908d11688030018b12e8753eee3b2016c1f0f24f4070a0b9c14fcef35ef55a23215a316ceaa5d1cc48e98e172be0")),
    Z: Fp7.create(BigInt(11))
  });
  var ut_root = Fp62.create({ c0: Fp22.ZERO, c1: Fp22.ONE, c2: Fp22.ZERO });
  var wsq = Fp12.create({ c0: ut_root, c1: Fp62.ZERO });
  var wcu = Fp12.create({ c0: Fp62.ZERO, c1: ut_root });
  var [wsq_inv, wcu_inv] = Fp12.invertBatch([wsq, wcu]);
  function psi(x, y) {
    const x2 = Fp12.mul(Fp12.frobeniusMap(Fp12.multiplyByFp2(wsq_inv, x), 1), wsq).c0.c0;
    const y2 = Fp12.mul(Fp12.frobeniusMap(Fp12.multiplyByFp2(wcu_inv, y), 1), wcu).c0.c0;
    return [x2, y2];
  }
  function G2psi(c, P3) {
    const affine = P3.toAffine();
    const p = psi(affine.x, affine.y);
    return new c(p[0], p[1], Fp22.ONE);
  }
  var PSI2_C1 = BigInt("0x1a0111ea397fe699ec02408663d4de85aa0d857d89759ad4897d29650fb85f9b409427eb4f49fffd8bfd00000000aaac");
  function psi2(x, y) {
    return [Fp22.mul(x, PSI2_C1), Fp22.neg(y)];
  }
  function G2psi2(c, P3) {
    const affine = P3.toAffine();
    const p = psi2(affine.x, affine.y);
    return new c(p[0], p[1], Fp22.ONE);
  }
  var htfDefaults = Object.freeze({
    // DST: a domain separation tag
    // defined in section 2.2.5
    // Use utils.getDSTLabel(), utils.setDSTLabel(value)
    DST: "BLS_SIG_BLS12381G2_XMD:SHA-256_SSWU_RO_NUL_",
    encodeDST: "BLS_SIG_BLS12381G2_XMD:SHA-256_SSWU_RO_NUL_",
    // p: the characteristic of F
    //    where F is a finite field of characteristic p and order q = p^m
    p: Fp7.ORDER,
    // m: the extension degree of F, m >= 1
    //     where F is a finite field of characteristic p and order q = p^m
    m: 2,
    // k: the target security level for the suite in bits
    // defined in section 5.1
    k: 128,
    // option to use a message that has already been processed by
    // expand_message_xmd
    expand: "xmd",
    // Hash functions for: expand_message_xmd is appropriate for use with a
    // wide range of hash functions, including SHA-2, SHA-3, BLAKE2, and others.
    // BBS+ uses blake2: https://github.com/hyperledger/aries-framework-go/issues/2247
    hash: sha256
  });
  var COMPRESSED_ZERO = setMask(Fp7.toBytes(_0n10), { infinity: true, compressed: true });
  function parseMask(bytes2) {
    bytes2 = bytes2.slice();
    const mask = bytes2[0] & 224;
    const compressed = !!(mask >> 7 & 1);
    const infinity = !!(mask >> 6 & 1);
    const sort = !!(mask >> 5 & 1);
    bytes2[0] &= 31;
    return { compressed, infinity, sort, value: bytes2 };
  }
  function setMask(bytes2, mask) {
    if (bytes2[0] & 224)
      throw new Error("setMask: non-empty mask");
    if (mask.compressed)
      bytes2[0] |= 128;
    if (mask.infinity)
      bytes2[0] |= 64;
    if (mask.sort)
      bytes2[0] |= 32;
    return bytes2;
  }
  function signatureG1ToRawBytes(point) {
    point.assertValidity();
    const isZero = point.equals(bls12_381.G1.ProjectivePoint.ZERO);
    const { x, y } = point.toAffine();
    if (isZero)
      return COMPRESSED_ZERO.slice();
    const P3 = Fp7.ORDER;
    const sort = Boolean(y * _2n10 / P3);
    return setMask(numberToBytesBE(x, Fp7.BYTES), { compressed: true, sort });
  }
  function signatureG2ToRawBytes(point) {
    point.assertValidity();
    const len = Fp7.BYTES;
    if (point.equals(bls12_381.G2.ProjectivePoint.ZERO))
      return concatBytes(COMPRESSED_ZERO, numberToBytesBE(_0n10, len));
    const { x, y } = point.toAffine();
    const { re: x0, im: x1 } = Fp22.reim(x);
    const { re: y0, im: y1 } = Fp22.reim(y);
    const tmp = y1 > _0n10 ? y1 * _2n10 : y0 * _2n10;
    const sort = Boolean(tmp / Fp7.ORDER & _1n11);
    const z2 = x0;
    return concatBytes(setMask(numberToBytesBE(x1, len), { sort, compressed: true }), numberToBytesBE(z2, len));
  }
  var bls12_381 = bls({
    // Fields
    fields: {
      Fp: Fp7,
      Fp2: Fp22,
      Fp6: Fp62,
      Fp12,
      Fr
    },
    // G1 is the order-q subgroup of E1(Fp) : y² = x³ + 4, #E1(Fp) = h1q, where
    // characteristic; z + (z⁴ - z² + 1)(z - 1)²/3
    G1: {
      Fp: Fp7,
      // cofactor; (z - 1)²/3
      h: BigInt("0x396c8c005555e1568c00aaab0000aaab"),
      // generator's coordinates
      // x = 3685416753713387016781088315183077757961620795782546409894578378688607592378376318836054947676345821548104185464507
      // y = 1339506544944476473020471379941921221584933875938349620426543736416511423956333506472724655353366534992391756441569
      Gx: BigInt("0x17f1d3a73197d7942695638c4fa9ac0fc3688c4f9774b905a14e3a3f171bac586c55e83ff97a1aeffb3af00adb22c6bb"),
      Gy: BigInt("0x08b3f481e3aaa0f1a09e30ed741d8ae4fcf5e095d5d00af600db18cb2c04b3edd03cc744a2888ae40caa232946c5e7e1"),
      a: Fp7.ZERO,
      b: _4n4,
      htfDefaults: { ...htfDefaults, m: 1, DST: "BLS_SIG_BLS12381G1_XMD:SHA-256_SSWU_RO_NUL_" },
      wrapPrivateKey: true,
      allowInfinityPoint: true,
      // Checks is the point resides in prime-order subgroup.
      // point.isTorsionFree() should return true for valid points
      // It returns false for shitty points.
      // https://eprint.iacr.org/2021/1130.pdf
      isTorsionFree: (c, point) => {
        const cubicRootOfUnityModP = BigInt("0x5f19672fdf76ce51ba69c6076a0f77eaddb3a93be6f89688de17d813620a00022e01fffffffefffe");
        const phi = new c(Fp7.mul(point.px, cubicRootOfUnityModP), point.py, point.pz);
        const xP = point.multiplyUnsafe(bls12_381.params.x).negate();
        const u2P = xP.multiplyUnsafe(bls12_381.params.x);
        return u2P.equals(phi);
      },
      // Clear cofactor of G1
      // https://eprint.iacr.org/2019/403
      clearCofactor: (_c, point) => {
        return point.multiplyUnsafe(bls12_381.params.x).add(point);
      },
      mapToCurve: (scalars) => {
        const { x, y } = G1_SWU(Fp7.create(scalars[0]));
        return isogenyMapG1(x, y);
      },
      fromBytes: (bytes2) => {
        const { compressed, infinity, sort, value } = parseMask(bytes2);
        if (value.length === 48 && compressed) {
          const P3 = Fp7.ORDER;
          const compressedValue = bytesToNumberBE(value);
          const x = Fp7.create(compressedValue & Fp7.MASK);
          if (infinity) {
            if (x !== _0n10)
              throw new Error("G1: non-empty compressed point at infinity");
            return { x: _0n10, y: _0n10 };
          }
          const right = Fp7.add(Fp7.pow(x, _3n5), Fp7.create(bls12_381.params.G1b));
          let y = Fp7.sqrt(right);
          if (!y)
            throw new Error("Invalid compressed G1 point");
          if (y * _2n10 / P3 !== BigInt(sort))
            y = Fp7.neg(y);
          return { x: Fp7.create(x), y: Fp7.create(y) };
        } else if (value.length === 96 && !compressed) {
          const x = bytesToNumberBE(value.subarray(0, Fp7.BYTES));
          const y = bytesToNumberBE(value.subarray(Fp7.BYTES));
          if (infinity) {
            if (x !== _0n10 || y !== _0n10)
              throw new Error("G1: non-empty point at infinity");
            return bls12_381.G1.ProjectivePoint.ZERO.toAffine();
          }
          return { x: Fp7.create(x), y: Fp7.create(y) };
        } else {
          throw new Error("Invalid point G1, expected 48/96 bytes");
        }
      },
      toBytes: (c, point, isCompressed) => {
        const isZero = point.equals(c.ZERO);
        const { x, y } = point.toAffine();
        if (isCompressed) {
          if (isZero)
            return COMPRESSED_ZERO.slice();
          const P3 = Fp7.ORDER;
          const sort = Boolean(y * _2n10 / P3);
          return setMask(numberToBytesBE(x, Fp7.BYTES), { compressed: true, sort });
        } else {
          if (isZero) {
            const x2 = concatBytes(new Uint8Array([64]), new Uint8Array(2 * Fp7.BYTES - 1));
            return x2;
          } else {
            return concatBytes(numberToBytesBE(x, Fp7.BYTES), numberToBytesBE(y, Fp7.BYTES));
          }
        }
      },
      ShortSignature: {
        fromHex(hex) {
          const { infinity, sort, value } = parseMask(ensureBytes("signatureHex", hex, 48));
          const P3 = Fp7.ORDER;
          const compressedValue = bytesToNumberBE(value);
          if (infinity)
            return bls12_381.G1.ProjectivePoint.ZERO;
          const x = Fp7.create(compressedValue & Fp7.MASK);
          const right = Fp7.add(Fp7.pow(x, _3n5), Fp7.create(bls12_381.params.G1b));
          let y = Fp7.sqrt(right);
          if (!y)
            throw new Error("Invalid compressed G1 point");
          const aflag = BigInt(sort);
          if (y * _2n10 / P3 !== aflag)
            y = Fp7.neg(y);
          const point = bls12_381.G1.ProjectivePoint.fromAffine({ x, y });
          point.assertValidity();
          return point;
        },
        toRawBytes(point) {
          return signatureG1ToRawBytes(point);
        },
        toHex(point) {
          return bytesToHex(signatureG1ToRawBytes(point));
        }
      }
    },
    // G2 is the order-q subgroup of E2(Fp²) : y² = x³+4(1+√−1),
    // where Fp2 is Fp[√−1]/(x2+1). #E2(Fp2 ) = h2q, where
    // G² - 1
    // h2q
    G2: {
      Fp: Fp22,
      // cofactor
      h: BigInt("0x5d543a95414e7f1091d50792876a202cd91de4547085abaa68a205b2e5a7ddfa628f1cb4d9e82ef21537e293a6691ae1616ec6e786f0c70cf1c38e31c7238e5"),
      Gx: Fp22.fromBigTuple([
        BigInt("0x024aa2b2f08f0a91260805272dc51051c6e47ad4fa403b02b4510b647ae3d1770bac0326a805bbefd48056c8c121bdb8"),
        BigInt("0x13e02b6052719f607dacd3a088274f65596bd0d09920b61ab5da61bbdc7f5049334cf11213945d57e5ac7d055d042b7e")
      ]),
      // y =
      // 927553665492332455747201965776037880757740193453592970025027978793976877002675564980949289727957565575433344219582,
      // 1985150602287291935568054521177171638300868978215655730859378665066344726373823718423869104263333984641494340347905
      Gy: Fp22.fromBigTuple([
        BigInt("0x0ce5d527727d6e118cc9cdc6da2e351aadfd9baa8cbdd3a76d429a695160d12c923ac9cc3baca289e193548608b82801"),
        BigInt("0x0606c4a02ea734cc32acd2b02bc28b99cb3e287e85a763af267492ab572e99ab3f370d275cec1da1aaa9075ff05f79be")
      ]),
      a: Fp22.ZERO,
      b: Fp22.fromBigTuple([_4n4, _4n4]),
      hEff: BigInt("0xbc69f08f2ee75b3584c6a0ea91b352888e2a8e9145ad7689986ff031508ffe1329c2f178731db956d82bf015d1212b02ec0ec69d7477c1ae954cbc06689f6a359894c0adebbf6b4e8020005aaa95551"),
      htfDefaults: { ...htfDefaults },
      wrapPrivateKey: true,
      allowInfinityPoint: true,
      mapToCurve: (scalars) => {
        const { x, y } = G2_SWU(Fp22.fromBigTuple(scalars));
        return isogenyMapG2(x, y);
      },
      // Checks is the point resides in prime-order subgroup.
      // point.isTorsionFree() should return true for valid points
      // It returns false for shitty points.
      // https://eprint.iacr.org/2021/1130.pdf
      isTorsionFree: (c, P3) => {
        return P3.multiplyUnsafe(bls12_381.params.x).negate().equals(G2psi(c, P3));
      },
      // Maps the point into the prime-order subgroup G2.
      // clear_cofactor_bls12381_g2 from cfrg-hash-to-curve-11
      // https://eprint.iacr.org/2017/419.pdf
      // prettier-ignore
      clearCofactor: (c, P3) => {
        const x = bls12_381.params.x;
        let t1 = P3.multiplyUnsafe(x).negate();
        let t2 = G2psi(c, P3);
        let t3 = P3.double();
        t3 = G2psi2(c, t3);
        t3 = t3.subtract(t2);
        t2 = t1.add(t2);
        t2 = t2.multiplyUnsafe(x).negate();
        t3 = t3.add(t2);
        t3 = t3.subtract(t1);
        const Q = t3.subtract(P3);
        return Q;
      },
      fromBytes: (bytes2) => {
        const { compressed, infinity, sort, value } = parseMask(bytes2);
        if (!compressed && !infinity && sort || // 00100000
        !compressed && infinity && sort || // 01100000
        sort && infinity && compressed) {
          throw new Error("Invalid encoding flag: " + (bytes2[0] & 224));
        }
        const L = Fp7.BYTES;
        const slc = (b, from, to) => bytesToNumberBE(b.slice(from, to));
        if (value.length === 96 && compressed) {
          const b = bls12_381.params.G2b;
          const P3 = Fp7.ORDER;
          if (infinity) {
            if (value.reduce((p, c) => p !== 0 ? c + 1 : c, 0) > 0) {
              throw new Error("Invalid compressed G2 point");
            }
            return { x: Fp22.ZERO, y: Fp22.ZERO };
          }
          const x_1 = slc(value, 0, L);
          const x_0 = slc(value, L, 2 * L);
          const x = Fp22.create({ c0: Fp7.create(x_0), c1: Fp7.create(x_1) });
          const right = Fp22.add(Fp22.pow(x, _3n5), b);
          let y = Fp22.sqrt(right);
          const Y_bit = y.c1 === _0n10 ? y.c0 * _2n10 / P3 : y.c1 * _2n10 / P3 ? _1n11 : _0n10;
          y = sort && Y_bit > 0 ? y : Fp22.neg(y);
          return { x, y };
        } else if (value.length === 192 && !compressed) {
          if (infinity) {
            if (value.reduce((p, c) => p !== 0 ? c + 1 : c, 0) > 0) {
              throw new Error("Invalid uncompressed G2 point");
            }
            return { x: Fp22.ZERO, y: Fp22.ZERO };
          }
          const x1 = slc(value, 0, L);
          const x0 = slc(value, L, 2 * L);
          const y1 = slc(value, 2 * L, 3 * L);
          const y0 = slc(value, 3 * L, 4 * L);
          return { x: Fp22.fromBigTuple([x0, x1]), y: Fp22.fromBigTuple([y0, y1]) };
        } else {
          throw new Error("Invalid point G2, expected 96/192 bytes");
        }
      },
      toBytes: (c, point, isCompressed) => {
        const { BYTES: len, ORDER: P3 } = Fp7;
        const isZero = point.equals(c.ZERO);
        const { x, y } = point.toAffine();
        if (isCompressed) {
          if (isZero)
            return concatBytes(COMPRESSED_ZERO, numberToBytesBE(_0n10, len));
          const flag = Boolean(y.c1 === _0n10 ? y.c0 * _2n10 / P3 : y.c1 * _2n10 / P3);
          return concatBytes(setMask(numberToBytesBE(x.c1, len), { compressed: true, sort: flag }), numberToBytesBE(x.c0, len));
        } else {
          if (isZero)
            return concatBytes(new Uint8Array([64]), new Uint8Array(4 * len - 1));
          const { re: x0, im: x1 } = Fp22.reim(x);
          const { re: y0, im: y1 } = Fp22.reim(y);
          return concatBytes(numberToBytesBE(x1, len), numberToBytesBE(x0, len), numberToBytesBE(y1, len), numberToBytesBE(y0, len));
        }
      },
      Signature: {
        // TODO: Optimize, it's very slow because of sqrt.
        fromHex(hex) {
          const { infinity, sort, value } = parseMask(ensureBytes("signatureHex", hex));
          const P3 = Fp7.ORDER;
          const half = value.length / 2;
          if (half !== 48 && half !== 96)
            throw new Error("Invalid compressed signature length, must be 96 or 192");
          const z1 = bytesToNumberBE(value.slice(0, half));
          const z2 = bytesToNumberBE(value.slice(half));
          if (infinity)
            return bls12_381.G2.ProjectivePoint.ZERO;
          const x1 = Fp7.create(z1 & Fp7.MASK);
          const x2 = Fp7.create(z2);
          const x = Fp22.create({ c0: x2, c1: x1 });
          const y2 = Fp22.add(Fp22.pow(x, _3n5), bls12_381.params.G2b);
          let y = Fp22.sqrt(y2);
          if (!y)
            throw new Error("Failed to find a square root");
          const { re: y0, im: y1 } = Fp22.reim(y);
          const aflag1 = BigInt(sort);
          const isGreater = y1 > _0n10 && y1 * _2n10 / P3 !== aflag1;
          const isZero = y1 === _0n10 && y0 * _2n10 / P3 !== aflag1;
          if (isGreater || isZero)
            y = Fp22.neg(y);
          const point = bls12_381.G2.ProjectivePoint.fromAffine({ x, y });
          point.assertValidity();
          return point;
        },
        toRawBytes(point) {
          return signatureG2ToRawBytes(point);
        },
        toHex(point) {
          return bytesToHex(signatureG2ToRawBytes(point));
        }
      }
    },
    params: {
      x: BLS_X,
      // The BLS parameter x for BLS12-381
      r: Fr.ORDER
      // order; z⁴ − z² + 1; CURVE.n from other curves
    },
    htfDefaults,
    hash: sha256,
    randomBytes
  });

  // input.js
  var utils = { bytesToHex, concatBytes, hexToBytes, utf8ToBytes };
  return __toCommonJS(input_exports);
})();
/*! noble-curves - MIT License (c) 2022 Paul Miller (paulmillr.com) */
/*! Bundled license information:

@noble/hashes/esm/utils.js:
  (*! noble-hashes - MIT License (c) 2022 Paul Miller (paulmillr.com) *)
*/
Array.prototype.base64url_encode = function() {
    return btoa(Array.from(new Uint8Array(this), b => String.fromCharCode(b)).join(''))
        .replace(/\+/g, '-')
        .replace(/\//g, '_')
        .replace(/=+$/, '');
}

ArrayBuffer.prototype.base64url_encode = function() {
    return btoa(Array.from(new Uint8Array(this), b => String.fromCharCode(b)).join(''))
        .replace(/\+/g, '-')
        .replace(/\//g, '_')
        .replace(/=+$/, '');
}

String.prototype.base64url_decode = function () {
    const m = this.length % 4;
    return Uint8Array.from(atob(
        this.replace(/-/g, '+')
            .replace(/_/g, '/')
            .padEnd(this.length + (m === 0 ? 0 : 4 - m), '=')
    ), c => c.charCodeAt(0))
}

Document.prototype.csrf = function () {
	let meta = document.querySelector("meta[name='csrf-token']")
	if(!!meta)
		if(!!meta.getAttribute("content"))
			meta = meta.getAttribute("content")
		else
			meta = String()
	return meta
}

Document.prototype.meta = function (name) {
	let meta = document.querySelector("meta[name='x-key-" + name + "']")
	if(!!meta)
		if(!!meta.getAttribute("content"))
			meta = meta.getAttribute("content").unhexlify()
		else
			meta = String()
	return meta
}

BigInt.prototype.bytes = function () {
		const big0 = BigInt(0)
		const big1 = BigInt(1)
		const big8 = BigInt(8)
		let big = this
		if (big < big0) {
		const bigint = (BigInt(big.toString(2).length) / big8 + big1) * big8
				bigint = big1 << bits
		big += prefix1
	}
	let hex = big.toString(16)
	if (hex.length % 2) {
		hex = '0' + hex
	}
	const len = hex.length / 2
	const u8 = new Uint8Array(len)
	var i = 0
	var j = 0
	while (i < len) {
		u8[i] = parseInt(hex.slice(j, j + 2), 16)
		i += 1
		j += 2
	}
	return u8.reverse()
}

Number.prototype.to_bytes = function (max) {
	if(!Number.isSafeInteger(Number(this))) {
		throw new Error("Number is out of range");
	}
	const size = this === 0 ? 0 : parseInt(this).byteLength();
	const bytes = new Uint8Array(size);
	let x = this;
	for (let i = (size - 1); i >= 0; i--) {
		const rightByte = x & 0xff;
		bytes[i] = rightByte;
		x = Math.floor(x / 0x100);
	}
	return new Uint8Array(max).fill((new Uint8Array(bytes.buffer)).reverse());
}

Number.prototype.to_bits = function () {
	return this * 8;
}

Number.prototype.bitLength = function () {
	return Math.floor(Math.log2(this)) + 1;
}

Number.prototype.byteLength = function () {
	return Math.ceil(parseInt(this).bitLength() / 8);
}

String.prototype.bytes = function () {
	return new TextEncoder().encode(this)
}

String.prototype.unhexlify = function () {
	 let result = [];
	 if(this.length){
		 let hexString = this;
		 while (hexString.length >= 2) { 
				 result.push(parseInt(hexString.substring(0, 2), 16));
				 hexString = hexString.substring(2, hexString.length);
		 }
	 }
	 return new Uint8Array(result);
}

String.prototype.hexlify = function () {
	if(this.length && this.hexlified())
		return this
	return String()
}

String.prototype.hexlified = function () {
	return /[0-9A-Fa-f]{6}/g.test(this);
}

Uint8Array.prototype.text = function() {
	return String.fromCharCode.apply(null, this);
}

Uint8Array.prototype.sum = function() {
	let total = 0,
				i = 0, length = this.length;
		while(i < this.length) 
			total += this[i++];
	return total
}

Uint8Array.prototype.append = function(array){
	let tmp = new Uint8Array(this.length + array.length);
		tmp.set(this);
		tmp.set(new Uint8Array(array), this.length);
	return tmp
}

Uint8Array.prototype.fill = function(array) {
	let i = 0;
		while(i < array.length){
			this[i] = array[i];
			i++;
		}
		return this
}

Uint8Array.prototype.equal = function(array) {
	if (!array || this.length !== array.length) {
		return false;
	}
	for (let i = 0; i < array.length; i++) {
		if (this[i] !== array[i]) {
			return false;
		}
	}
	return true;
}

Uint8Array.prototype.long = function() {
	let result = BigInt(0);
	for (let i = this.length - 1; i >= 0; i--) {
		result = result * BigInt(256) + BigInt(this[i]);
	}
	return result
}

Uint8Array.prototype.empty = function() {
	if(this.long() === 0n)
		return true
	return false
}

Uint8Array.prototype.hexlify = function(){ 
	return Array.from(this)
	.map((i) => i.toString(16).padStart(2, '0'))
	.join('');
}


Math.powMod = function(a, e, m) {
	// h/t https://umaranis.com/2018/07/12/calculate-modular-exponentiation-powermod-in-javascript-ap-n/
	if (m === 1n)
	return 0n;
	if (e < 0n)
	return Math.powMod(Math.modInv(a, m), -e, m);
	for (var b = 1n; e; e >>= 1n) {
	if (e % 2n === 1n)
		b = (b * a) % m;
	a = (a * a) % m;
	}
	return b;
}

Math.modInv = function(a, m) {
	// h/t https://github.com/python/cpython/blob/v3.8.0/Objects/longobject.c#L4184
	const m0 = m;
	var b = 1n, c = 0n, q, r;
	while (m) {
	[q, r] = [a/m, a%m];
	[a, b, c, m] = [m, c, b - q*c, r];
	}
	if (a !== 1n)
	throw new RangeError("Not invertible");
	if (b < 0n)
	b += m0;
	return b;
}

	class GCM{

		__material = new Uint8Array()

		constructor(...args){
			if(args[0] && !this.key)
				this.key = this.importKey(args[0])
			if(args[1])
				this.aead = new Uint8Array(args[1])
			else
				this.aead = new Uint8Array(16)
		}

		async importKey(key) {
			this.__material = new Uint8Array(key)
			return window.crypto.subtle.importKey('raw',
										this.__material, 
										{ name: "AES-GCM", 
										  length: parseInt(this.__material.length).to_bits() },
										false,
										["encrypt", "decrypt"]);
		}

		async grindKey(salt = new Uint8Array(16), info = new Uint8Array()){
			let key = await window.crypto.subtle.importKey('raw',
										this.__material, 
										'HKDF',
										false,
										["deriveBits", "deriveKey"]);
			this.key = await window.crypto.subtle.deriveKey({
									name: "HKDF",
									salt: salt,
									info: info,
									hash: "SHA-256"},
									key,
									{ name: "AES-GCM", length: key.algorithm.length },
									true,
									["encrypt", "decrypt"]);
		}

		async encrypt(data) {
			let iv = nobleHashes.utils.randomBytes(12)
			return await window.crypto.subtle.encrypt(
				{
					name: "AES-GCM",
					iv: iv,
					additionalData: this.aead,
					tagLength: parseInt(this.aead.length).to_bits()
				},
				await this.key,
				data,
			).then((ciphertext) => {
				return iv.append(new Uint8Array(ciphertext));
			  })
			 .catch((error) => {
				throw new Error('Encryption faild!')
			  });
		}

		async decrypt(data) {
			return await window.crypto.subtle.decrypt(
				{
					name: "AES-GCM",
					iv: data.slice(0, 12),
					additionalData: this.aead,
					tagLength: parseInt(this.aead.length).to_bits()
				},
				await this.key,
				data.slice(12, data.byteLength),
			).then((data) => {
				return new Uint8Array(data)
			 })
			 .catch((error) => {
			 	return new Uint8Array()
			 });
		}
	}HTMLCollection.prototype.forEach = Array.prototype.forEach;

const observer = new PerformanceObserver((list) => {
	list.getEntries().forEach((entry) => {
		console.log(
			'The time to ' + entry.name + ' was %c' + Math.round(entry.startTime), "color: #bada55", 'milliseconds.',
		);
	});
});

observer.observe({ type: "paint", buffered: true }, {type: "navigation", buffered: true});

window.addEventListener('load', (event) => {
	let time = window.performance.timing;
	let pageloadtime = time.loadEventStart - time.navigationStart;
	console.log(
		'The time to interactive was %c' + Math.round(pageloadtime), "color: #bada55", `milliseconds.`,
	);
});

document.addEventListener("DOMContentLoaded", (event) => {
	let time = window.performance.timing;
	let speed = time.domInteractive - time.domLoading;
	console.log(
		'The DOMContentLoaded take %c' + speed, "color: #bada55", `milliseconds.`,
	);
});

console.image = async function(url, size = 100) {
	const image = new Image();
	image.src = url;
	image.onload = function() {
		var style = [
			'font-size: 1px;',
			'padding: ' + this.height/100*size + 'px ' + this.width/100*size + 'px;',
			'background: url('+ url +') no-repeat;',
			'background-size: contain;'
		 ].join(' ');
		 console.log('%c ', style);
	};
};

const url = 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAAA4CAMAAAA8cK3qAAAAjVBMVEVHcEzy7+329vf+/v7r4Nv8/f3+/v77+/vr5uX5+fn09fX19fb7+/z+/v78/P3+/v7////8/Pz6+vr4+Pnv7/D+/v7+/v7+/v79/f76+vr/kU3+/v79/f36+vv7+/v4+Pj9/f37+/v6+vr8/Pz9/f3vjEz2j033j0z9kU38kU33j035kE34kE3///9HcEwi/9nXAAAAL3RSTlMAEByPCnb8iQSQJ3FwscXu9n5ULk/nvODOR/7YmGlhM6Y4Pp6cIV6B492Xk4v/AMZKE0YAAAKnSURBVFjD7ZbZdqMwDIZt4wCBmJ0ABQKhaTub3//1RrJZQsgyF72Zc/zfsMn6JEtWQoiRkZGRkdEkl3PufpPVQ7VBECQvrfx/snooR0q5e2m1B6uDgXwHxEURQpnuDOp1Hn0Cuf3usjTVS2fI6PFamRDixE9BwNDFIcjDPNixBxAvLlff3awvwrAWibtAWAMe/TXFh28Xy5Y1LPSOUuvo3YUM5fg96HRaVqSfI4fPELTOz2QDyW2JEIaMKMSFgt6BpLWcVGIUrjM/9zOkCsFHS7YQKQthURJjjEmaBHBttxC3h2to+Q24kRbR/mTttE1Yp9N2MVz8zu9A7MaDUjEItEgx4gI2jG4gZ4zxBM8HSLzwNLTEBVU1F96Z0txAhCInsLZR7y4QcbqB7LBYaEmxNCfiQSxRsm5hTC7cDhd/zJ2o3bLOwzCcG0guuYWowGP1woK7PakiVclriIOb5bhPIA2WHeoeRtG6KBrCjyp+FObUk9OU2QLBDspT8gKyaHcPYmvIYYaINUQpfgZBq6Mzadhsl5jnBm7su6phSW8gmEr3BNKqnX48u/bKNSFTdbDbwm4NEb0+NA8huGgspP6Jcz+/PvkCSXTnEtLlULxKN5mFlpSOkDpN81XLbSAc96MHCh+EMvt6e3v7WiAMnYqUdtgBAdW7FsWMpn3DNSTWl4A9hIwn+N0SocQj/PEDID8/lrHS2thAZS7HYBVVFvAC58g4VvD0bGp/BSGHaOqQMLsD4db02dZnoSqmFzAgpgGJ+RU3tfdt257K7SalrYbqsQIn7m+A/IEbB0xUR9NYe60PY2nPQoUVCZi6e7Dy8eeghJub6cWyLFtmDUucSxNXujHp5y9VeG8x8Vrrsj8t9rSKm4u2RytViw5uBm7+SRoZGRkZ/V/6CyFVcb3QgLeDAAAAAElFTkSuQmCC'
console.image(url, 23);

"use strict";
var relock = (() => {

	var __defProp = Object.defineProperty;
	var __getOwnPropDesc = Object.getOwnPropertyDescriptor;
	var __getOwnPropNames = Object.getOwnPropertyNames;
	var __hasOwnProp = Object.prototype.hasOwnProperty;

	var __export = (target, all) => {
		for (var name in all)
			__defProp(target, name, { get: all[name], enumerable: true });
	};
	var __copyProps = (to, from, except, desc) => {
		if (from && typeof from === "object" || typeof from === "function") {
			for (let key of __getOwnPropNames(from))
				if (!__hasOwnProp.call(to, key) && key !== except)
					__defProp(to, key, { get: () => from[key], enumerable: !(desc = __getOwnPropDesc(from, key)) || desc.enumerable });
		}
		return to;
	};
	var __toCommonJS = (mod2) => __copyProps(__defProp({}, "__esModule", { value: true }), mod2);
	var input_exports = {};

	class Montgomery{

		x25519   = nobleCurves.x25519
		ed25519  = nobleCurves.ed25519

		constructor(key){
			this.private = nobleCurves.ed25519_edwardsToMontgomeryPriv(key);
			this.public = nobleCurves.ed25519_edwardsToMontgomeryPub(this.ed25519.getPublicKey(key));
		}

		secret(key){
			return this.x25519.getSharedSecret(this.private, key)
		}
	}

	class Signature{

		ed25519  = nobleCurves.ed25519

		constructor(key){
			if(!key.length)
				this.private = this.ed25519.utils.randomPrivateKey();
			else
				this.private = key;
			this.public = this.ed25519.getPublicKey(this.private)
		}

		bytes(){
			return this.private
		}
	}

	class Idle {
			constructor(timeout = 10, idleCallback = null, backToActiveCallback = null) {
					this.timeout = timeout * 1000
					this.timestamp = new Date()
					this.idleCallback = idleCallback
					this.backToActiveCallback = backToActiveCallback
					this.idle = false
					this.timer = null
					this.events = ['scroll', 'mousemove', 'touchstart', 'focus']
					console.info('Initiate activity monitoring and re-keying engine.')
			let timestamp = document.querySelector("meta[name='x-key-timestamp']")
			if(timestamp === null)
				timestamp = String()
			if(!!timestamp) {
				if(!!timestamp.getAttribute("content"))
					timestamp = timestamp.getAttribute("content")
				else
					timestamp = String()
				if(timestamp)
					this.timestamp = new Date(parseInt(timestamp) * 1000)
			}
			window.addEventListener('visibilitychange', function(event) {
				if(!document.hidden){
					if(new Date() - this.timestamp > this.timeout) {
						this.goIdle()
					}
					this.processTimestamp()
				}
			}.bind(this), false);
					this.init()
			}

			init() {
					this.events.forEach(name => {
						window.addEventListener(name, this.processTimestamp, true)
					})

					this.interval = setInterval(() => {
						if(new Date() - this.timestamp > this.timeout) {
							this.goIdle()
						}
					}, 1000)
			}

			goIdle = () => {
				if(!this.idle){
						this.idle = true
				document.dispatchEvent(new CustomEvent('XSiteIdle', {bubbles: true, 
																	 detail:{ timeout: this.timeout / 1000 }}));
				}
			}

			processTimestamp = (event) => {
				if(this.idle) {
					this.timestamp = new Date()
					this.idle = false
					document.dispatchEvent(new CustomEvent('XSiteActive', {bubbles: true}));
				}
			}
	}

	class Storage{

		__session   = new Uint8Array()
		__tesseract = new Uint8Array()

		constructor(...args){
			if(args[0] && args[0].length === 32){
				this.session = new Uint8Array(args[0])
			} else if(args[0] && args[0].length !== 32){
				this.session = new Uint8Array()
			}
			if(args[1] && args[1].length === 32) {
				new GCM(args[1]).decrypt(this.get('tesseract'))
					.then((tesseract) => {
						if(tesseract.length !== 0) {
							this.__tesseract = tesseract
							document.dispatchEvent(new CustomEvent('XKeyReady', {bubbles: true, detail:{ obj: true }}));
						} else {
							console.log('Recovery wrong key!');
							this.secret = nobleHashes.utils.randomBytes(128)
						}
					})
			} else if(this.established && this.__tesseract.length === 0) {
				console.log('Restored. Try to gain access to the local storage area.')
				this.session.decrypt(this.get('tesseract'))
					.then((tesseract) => {
						if(tesseract.length !== 0)
							this.__tesseract = tesseract
						document.dispatchEvent(new CustomEvent('XKeyReady', {bubbles: true, detail:{ obj: true }}));
					});
			}
		}

		get signer() {
			return this.get('signature').slice(0, 32)
		}

		set signer(key) {
			if(key && key.length)
				return this.set('signature', key)
			return this.signer
		}

		get client() {
			return this.get('client').slice(0, 32)
		}

		set client(key) {
			if(key && key.length)
				return this.set('client', key)
			return this.client
		}

		get xsid() {
			if(!localStorage.hasOwnProperty('xsid'))
				localStorage.setItem('xsid', new Uint8Array().hexlify())
			return localStorage.getItem('xsid').unhexlify()
		}

		set xsid(key) {
			if(key && key.length)
				localStorage.setItem('xsid', new Uint8Array(key).hexlify())
			return this.xsid
		}

		get secret() {
			return this.__tesseract
		}

		set secret(key) {
			this.__tesseract = key
			this.session.encrypt(key).then((encrypted) => {
				this.set('tesseract', encrypted)
				this.set('stamp', nobleHashes.blake2b(key, {salt: new Uint8Array(16), 
																dkLen: 16}))
				this.signer = this.__signature // save signature with new session
				document.dispatchEvent(new CustomEvent('XKeyReady', {bubbles: true, detail:{ obj: true }}));
				// this.session.decrypt(this.get('tesseract')).then((decrypted) => {
				// 	console.log('decrypt test', decrypted)
				// });
				// console.log('%c Oh my heavens! ', 'background: #222; color: #bada55', '%c We got match!', 'background: #222; color: #ff6600',);
				// console.log("%cI am red %cI am green", "color: #bada55", "color: green");
				console.log('Current Transient Key stamp:' + ' %c' + this.hash.hexlify(), "color: #bada55")
				console.log('Current Transient Key size is', this.__tesseract.length, 'bytes')
			});
		}

		get(name) {
			if(!localStorage.hasOwnProperty(name))
				localStorage.setItem(name, new Uint8Array().hexlify())
			return localStorage.getItem(name).unhexlify()
		}

		set(name, value) {
			if(value && value.length)
				localStorage.setItem(name, new Uint8Array(value).hexlify())
			return this.get(name)
		}

		get session() {
			if(!sessionStorage.hasOwnProperty('relock'))
				sessionStorage.setItem('relock', new Uint8Array().hexlify())
			if(this.__session.length !== 32)
				this.__session = sessionStorage.getItem('relock').unhexlify()
			if(this.__session.length === 32)
				return new GCM(this.__session.slice(0,32))
			return false
		}

		set session(key) {
			if(key.length) {
				sessionStorage.setItem('relock', new Uint8Array(key).hexlify())
			} else {
				sessionStorage.removeItem('relock')
				this.__session = new Uint8Array()
				this.__tesseract = new Uint8Array()
			}
			return this.session
		}

		get established() {
			if(this.session)
				return true
			return false
		}

		get hash() {
			if(this.get('stamp').length !== 0)
				return this.get('stamp')
			return new Uint8Array()
		}

		clear() {
			localStorage.removeItem('signature')
			localStorage.removeItem('tesseract')
			localStorage.removeItem('server')
			localStorage.removeItem('stamp')
			localStorage.removeItem('client')
			localStorage.removeItem('xsid')
			sessionStorage.removeItem('relock')
			sessionStorage.removeItem('screen')
		}
	}

	class relock{

		ed25519  = nobleCurves.ed25519
		HKDF     = nobleHashes.hkdf
		blake    = nobleHashes.blake2b
		scrypt   = nobleHashes.scrypt
		random   = nobleHashes.utils.randomBytes

		__storage     = undefined
		__x25519      = undefined
		__signer      = undefined
		__established = false
		__XSiteIdle   = undefined
		__screen      = new Uint8Array()

		__refactor    = String()

		constructor(power = 128, ...args){

			this.nonce   = this.random(16)
			this.power   = power

			this.startLoading = window.performance.now()
			this.channel = new BroadcastChannel('tab-notifications');
			
			this.private = this.ed25519.utils.randomPrivateKey()
			this.public  = this.ed25519.getPublicKey(this.private)

			let xsid     = document.meta('xsid')
			let screen   = document.meta('screen')

			if(!this.screen.equal(screen) || !this.xsid.equal(xsid))
				this.__storage = new Storage(new Uint8Array())
			else
				this.__storage = new Storage(...args)

			this.__x25519    = new Montgomery(this.private)
			this.__signer    = new Signature(this.signer || this.private)
			
			if(!this.screen.equal(screen)){
				this.tab = new FormData()
				this.tab.append('origin', document.location.origin)
				this.tab.append('path', document.location.pathname)
				this.tab.append('screen', this.screen.hexlify())
				this.tab.append('wrong', screen.hexlify())
				navigator.sendBeacon('/relock/screen', this.tab)
			}

			document.addEventListener('XReKeying', function(event) {
				document.getElementsByClassName("keygen").forEach((el) => {
					el.style.visibility = "visible";
				});
			}.bind(this));

			document.addEventListener('XReKeyingStop', function(event) {
				setTimeout(() => {
					document.getElementsByClassName("keygen").forEach((el) => {
						el.style.visibility = "hidden";
					});
				}, 500)
			}.bind(this));

			document.addEventListener('XKeyValidate', this.KeyValidate.bind(this));
			document.addEventListener('XKeyReady', this.KeyReady.bind(this));

			document.addEventListener("DOMContentLoaded", function(event) {
				console.log('xsid is correct?', this.xsid.equal(xsid))
				console.log('screen is correct?', this.screen.equal(screen))
				if(!this.__storage.established)
					this.exchange()
			}.bind(this));

			window.addEventListener('beforeunload', function(event) {
				this.unload = new FormData()
				this.unload.append('screen', this.screen.hexlify())
				this.unload.append('origin', document.location.origin)
				this.unload.append('path', document.location.pathname)
			}.bind(this));

			window.addEventListener('visibilitychange', function(event) {
				if(document.hidden && this.unload)
					navigator.sendBeacon('/relock/close', this.unload)
			}.bind(this));

			window.addEventListener('XPasskeyCreated', function(event) {
				console.log(event)
			}.bind(this));
		}

		get id(){
			return this.client.hexlify()
		}

		get screen(){
			if(!sessionStorage.hasOwnProperty('screen'))
				sessionStorage.setItem('screen', this.random(16).hexlify())
			return sessionStorage.getItem('screen').unhexlify()
		}

		set screen(value){
			sessionStorage.setItem('screen', value.hexlify())
		}

		get xsid(){
			if(!localStorage.hasOwnProperty('xsid'))
				localStorage.setItem('xsid', this.random(32).hexlify())
			return localStorage.getItem('xsid').unhexlify()
		}

		get established () {
			return this.__established
		}

		get session(){
			return this.__storage.session
		}

		get secret(){
			return this.__storage.secret
		}

		get client(){
			return this.__storage.client
		}

		get signer(){
			return this.__storage.signer
		}

		get hash(){
			return this.__storage.hash
		}

		set credential(value) {
			navigator.credentials.create({
				password: {
					id: window.location.origin,     // The username or unique identifier for the account
					name: "Account recovery code for",
					password: value,   // The password
					mediation: 'silent'
				}
			}).then(function (credential) {
				console.log("Credential created:", credential);
				// Store the credential securely for later use, or handle as needed
				// Store it
				navigator.credentials.store(credential).then(function () {
				  // continuation
				});
			}).catch(function (err) {
				console.log("Error creating credential:", err);
			});
		}

		async KeyReady(event){
			this.__signer = new Signature(this.__storage.signer)
			if(this.__refactor) {
				console.log('XKeyInProgress, got re-keying demand.')
				console.log('Mutation in progress...')
				if(this.rekeying(this.__refactor)){
					this.__refactor = String()
					console.log('Re-keying by factor Successful.')
				} else { //if(this.close()){
					this.__refactor = String()
					console.warn('Re-keying faild, can\'t verify token. Session destroyed...')
				}
			} else {
				console.info('XKeyReady, access to the storage is active.')
				console.log(
					'The time to access storage took %c' + Math.round(window.performance.now() - this.startLoading), "color: #bada55", `milliseconds.`,
				);
				this.startLoading = window.performance.now()
				document.dispatchEvent(new CustomEvent('XKeyValidate', {bubbles: true, 
																		detail:{ rekeying: true }}));
			}
		}

		async KeyValidate(event){
			// window.dispatchEvent(new CustomEvent('XReKeying', {bubbles: true, detail:{ obj: true }}));
			let nonce = document.meta('nonce')
			let signature = document.meta('signature')

			if(nonce && signature && this.verify(nonce, signature)) {
				console.log('Discovered valid signature of re-keying demand.')
				document.querySelector("meta[name='x-key-signature']").remove()
				if(this.rekeying(nonce))
					console.log('The rolling of the Transient key in progress.')
			} else {
				if(nonce)
					document.querySelector("meta[name='x-key-nonce']").remove()
				this.request('/relock/validate', {nonce: nonce,
												  screen: this.screen.hexlify()})
					.then((response) => response.json())
					.then((data) => {
							this.__established = data.status

							if(data.status){
								console.log('Token match the server side, confirm status:', data.status)
								console.log(
									'The time to confirm keys was %c' + Math.round(window.performance.now() - this.startLoading), "color: #bada55", `milliseconds.`,
								);
							} else if(data.reprocess){
								console.log('Data reprocess clear')
								return this.clear()
							}

							// window.Passkeys.register()

							console.log('Token established:', this.__established)
							document.dispatchEvent(new CustomEvent('XReKeyingStop', {bubbles: true, 
																						 detail:{ rekeying: false,
																								  authenticated: data.authenticated,
																								  credential: data.credential,
																								  owner: data.owner,
																								  valid: data.status }}));
							if(this.__established){
								console.log('User is authenticated:', data.authenticated)
								window.dispatchEvent(new CustomEvent('XKeyEstablished', {bubbles: true, 
																						 detail:{ rekeying: false,
																								  authenticated: data.authenticated,
																								  credential: data.credential,
																								  owner: data.owner,
																								  valid: data.status }}));
							} else {
								window.dispatchEvent(new CustomEvent('XKeyFailure', {bubbles: true, 
																					 detail:{ rekeying: false,
																							  authenticated: data.authenticated,
																							  credential: data.credential,
																							  owner: data.owner,
																							  valid: data.status }}));
							}
					 })
					.catch((error) => {
						console.error('Request validation failure:', error);
						document.dispatchEvent(new CustomEvent('XReKeyingStop', {bubbles: true, 
																					 detail:{ rekeying: false,
																								valid: false }}));
					 });
			}
		}

		async exchange(){
			document.dispatchEvent(new CustomEvent('XReKeying', {bubbles: true, detail:{ exchange: true }}));
			if(!this.established && !this.__storage.established)
				this.request('/relock/exchange', {hash: this.hash,
												   key: this.public,
												  xsid: this.xsid,
												screen: this.screen,
												 width: window.innerWidth,
												height: window.innerHeight})
					.then((response) => response.json())
					.then((message) => {
						let client  = new Uint8Array(message.key)
						console.log('Key agreement in progress...')
						// console.log('Client public', this.public)
						let x25519  = nobleCurves.ed25519_edwardsToMontgomeryPub(client)
						let secret  = this.__x25519.secret(x25519)
						let session = this.derive(secret)

						if(!this.__storage.hash.length){
							this.__storage.session = session
							this.__storage.xsid    = new Uint8Array(message.xsid)
							this.__storage.client  = new Uint8Array(message.signer)
							this.__storage.secret  = this.expand(session, this.power)
							this.__storage.signer  = this.private
							this.__signer          = new Signature(this.private)
							// console.log('Server key', this.__storage.client)
							// console.log('Client', this.__signer.public)
							console.log('New keys establishment of', this.__storage.secret.length, 'accomplished.')
						} else {
							console.log('Recovery key delivered. Try to decrypt storage.')
							new GCM(session).decrypt(new Uint8Array(message.recovery))
								.then(decrypted => {									// if(!new Uint8Array(message.token).empty())
									if(message.token.length)
										this.__refactor = message.token
									if(message.restore)
										this.__storage  = new Storage(decrypted, decrypted)
									else
										this.__storage  = new Storage(session, decrypted)
									this.__storage.xsid = new Uint8Array(message.xsid)
									this.__signer = new Signature(this.__storage.signer)

								})
								.catch((error) => {
									// console.log('Decryption wrong key!');
									// return new Uint8Array()
									console.log(error)
								});

						}
						console.log('Exchange accomplished.')
					 })
					.catch((error) => {
						document.dispatchEvent(new CustomEvent('XReKeyingStop', {bubbles: true, detail:{ exchange: true }}));
						console.error('Key agreement failure.')
						console.log(error)
						// this.clear()
					 });
		}

		async request(path, body) {
			for (let index in body) {
				if(body[index] !== null && body[index].constructor == Uint8Array)
					body[index] = Array.from(body[index])
			};
			let token = this.token()
			let signature = this.sign(token)
			// 	// body['X-Key-Token'] = Array.from(token)
			// 	// body['X-Key-Signature'] = Array.from(this.sign(token))
			return fetch(path, {
					method: 'POST',
					headers: {'Content-Type': 'application/json',
							  'accept': 'application/json',
							  'X-Key-Token': token.hexlify(),
							  'X-Key-Signature': signature.hexlify(),
							  'X-Key-Time': Math.round(+new Date()/1000),
							  'Access-Control-Allow-Credentials': 'true',
							  'X-CSRFToken': document.csrf()},
					credentials: 'include',
					body: JSON.stringify(body)
				})
		}

		close(){
			this.__storage.session = new Uint8Array()
			window.setTimeout(() => { window.location.href = '/' }, 100)
			return true
		}

		clear(redirect){
			// alert('clear');
			this.request('/relock/clear', {keys: true})
				.then((response) => response.json())
				.then((data) => {
						this.__storage.clear()
					// if(!redirect)
					// 	setTimeout(() => { window.location.href = '/' }, 100)
				 })
				.catch((error) => {
					console.error('Token validation failure:', error);
				 });
		}

		rekeying(salt = new Uint8Array(32),
				 token = new Uint8Array(32)) {
			if(salt.constructor === String)
				salt   = salt.unhexlify()
			if(!salt.empty() && salt.length > 32)
				token  = salt.slice(salt.length / 2, salt.length)
			if(salt.empty())
				salt   = this.random(salt.length)
			else if(salt.length > 32)
				salt   = salt.slice(0, salt.length / 2)
			this.__storage.secret = this.derive(this.secret, salt, this.secret.length)
			if(!token.empty())
				return this.validate(token)
			return salt.append(this.token()).hexlify()
		}

		derive(key, salt = new Uint8Array(32), 
					size = 32,
					info = 'handshake data') {
			return this.HKDF(nobleHashes.sha256, key, salt, info, size);
		}

		expand(key, max = 128){
			let slice = new Uint8Array()
			while(slice.length < (max || key.sum())){
				let salt = key.sum().to_bytes(16)
					key  = this.blake(key, {salt: salt, 
											dkLen: 32})
				slice = slice.append(key);
			}
			return this.derive(slice, key.sum().to_bytes(16), slice.length)
		}

		x(x, basepoint = 13) {
			return parseInt(Math.powMod(BigInt(basepoint), BigInt(x), BigInt(this.secret.length - 1)))
		}

		get(p=0, l=0, r=32){
			if(this.secret.length !== 0){
				let g = Math.pow(this.secret[Math.round(this.secret.length/2)], 2)
				let x = this.x(p, g)
				if(this.secret.slice(x,x + r).length == r)
					return this.secret.slice(x,x + r) 
				else 
					return this.secret.slice(x-r,x)
			}
			return new Uint8Array()
		}

		token(size = 32){
			if(this.secret.length !== 0){
				let random = this.random(size / 2)
				let secret = this.get(random.slice(0, random.length - 1).long(), 
									  random.slice(random.length - 1, random.length).long())
					secret = this.scrypt(secret, random, 
									   { N: 2 ** 8,
										 r: 8,
										 p: 1,
										 dkLen: random.length });
				return random.append(secret)
			}
			return new Uint8Array()
		}

		validate(token = new Uint8Array(32)) {
			let random = token.slice(0, token.length / 2)
				token  = token.slice(token.length / 2,token.length)
			let secret = this.get(random.slice(0, token.length - 1).long(), 
								  random.slice(token.length - 1, token.length).long())
				secret = this.scrypt(secret, random, 
								{ N: 2 ** 8,
								  r: 8,
								  p: 1, 
								  dkLen: random.length });
			return secret.equal(token)
		}

		aead(random, salt = new Uint8Array(16), size = 16){
			let secret = this.get(random.slice(0, 3).long(), 
									random.slice(3, 4).long())
			return this.blake(secret, {salt: salt, 
										dkLen: size})
		}

		salt(random, salt = new Uint8Array(16), size = 16){
			let secret = this.get(random.slice(4, 7).long(), 
									random.slice(7, 8).long())
			return this.scrypt(secret, salt, 
								{ N: 2 ** 16, 
									r: 8, 
									p: 1, 
									dkLen: size });
		}

		key(random, salt = new Uint8Array(16), size = 32){
			let secret = this.get(random.slice(8, 11).long(),
									random.slice(11,12).long())
			if(!salt.empty())
				return this.blake(secret, {salt: salt, 
												 dkLen: size})
			return secret
		}

		sign(data){
			if(!data.length)
				return new Uint8Array()
			return this.ed25519.sign(data, this.__signer.private)
		}

		verify(data, signature){
			return this.ed25519.verify(signature, data, this.client); // Default mode: follows ZIP215
		}

		async deriveKey(keyMaterial, salt, length = 32) {
			let key = await window.crypto.subtle.importKey('raw',
										keyMaterial, 
										'HKDF',
										false,
										["deriveBits", "deriveKey"]);
			return window.crypto.subtle.deriveKey({
									name: "HKDF",
									salt: salt,
									info: new Uint8Array(),
									hash: "SHA-256"},
									key,
									{ name: "AES-GCM", length: length * 8 },
									true,
									["encrypt", "decrypt"]);
		}

		async encrypt(data) {
			let iv   = this.random(12)
			let salt = this.salt(iv)
			let aead = this.aead(iv, salt)
			let key  = this.key(iv)
					key  = await this.deriveKey(key, salt)
			let ciphertext = await window.crypto.subtle.encrypt(
				{
					name: "AES-GCM",
					iv: iv,
					additionalData: aead,
					tagLength: parseInt(aead.length).to_bits()
				},
				key,
				data,
			);
			return iv.append(new Uint8Array(ciphertext));
		}

		async decrypt(data) {
			data = new Uint8Array(data)
			let iv = data.slice(0, 12)
			let salt = this.salt(iv)
			let aead = this.aead(iv, salt)
			let key  = this.key(iv)
					key  = await this.deriveKey(key, salt)
			let ciphertext = data.slice(12, data.byteLength)
			
			data = await window.crypto.subtle.decrypt(
				{
					name: "AES-GCM",
					iv: iv,
					additionalData: aead,
					tagLength: parseInt(aead.length).to_bits()
				},
				key,
				ciphertext,
			);
			return new Uint8Array(data);
		}
	}

	let object = undefined

	try {
		object = new relock()
	}
	catch(err) {
		console.error('Fatal object start.', err)
	}
	finally{
		if(object){
			__export(input_exports, {
				id:          () => object.id,
					id:          () => object.hash,
					token:       () => object.token.bind(object),
					encrypt:     () => object.encrypt.bind(object),
					decrypt:     () => object.decrypt.bind(object),
					sign:        () => object.sign.bind(object),
					verify:      () => object.verify.bind(object),
					clear:       () => object.clear.bind(object),
					request:     () => object.request.bind(object),
					validate:    () => object.validate.bind(object),
					token:       () => object.token.bind(object),
					screen:      () => object.screen,
					public:      () => object.public
				});

			return __toCommonJS(input_exports);
		}
	}
})();window.addEventListener('XKeyEstablished', function(event) {
	const forms = document.querySelectorAll("form");
		  forms.forEach((form) => {
				let token = window.relock.token()
				var input = document.createElement("input");
					input.setAttribute("type", "hidden");
					input.setAttribute("name", "X-Key-Token");
					input.setAttribute("value", token.hexlify());
				form.appendChild(input);
				var input = document.createElement("input");
					input.setAttribute("type", "hidden");
					input.setAttribute("name", "X-Key-Signature");
					input.setAttribute("value", window.relock.sign(token).hexlify());
				form.appendChild(input);

				form.addEventListener('submit', function(event){
					let token = window.relock.token()
					let input = event.target.querySelector('input[name="X-Key-Token"]')
						input.setAttribute("value", token.hexlify());

					let signature = window.relock.token()
						input = event.target.querySelector('input[name="X-Key-Signature"]')
						input.setAttribute("value", window.relock.sign(token).hexlify());
				})
		  });
});