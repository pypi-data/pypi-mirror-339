# Breaking Changes: node 16 → 18
> Generated on: 2025-04-09T14:54:22.614316
> Stack: node
> Current Version: 16
> Upgrade Version: 18

# Comprehensive Guide to Breaking Changes, Deprecations, and API Modifications: Upgrading from Node.js 16 to Node.js 18

## 1. Summary of Major Changes
Node.js 18 introduces several new features, performance improvements, and breaking changes. Key updates include:
- Native support for the Fetch API.
- Introduction of the `node:test` module for built-in testing.
- OpenSSL 3 support, requiring updates to cryptographic operations.
- Changes to HTTP timeouts and DNS resolution defaults.
- Deprecation and removal of several APIs and undocumented features.
- Updated V8 engine (version 10.1) with new JavaScript features.
- Enhanced global APIs, including Web Streams and Blob.

## 2. Breaking Changes by Version

### **Node.js 17 (Intermediate Version)**
Node.js 17 introduced changes that impact the upgrade path to Node.js 18:
- **OpenSSL 3 Support**: Node.js 17 transitioned to OpenSSL 3, which may break cryptographic operations relying on older OpenSSL versions. Update cryptographic libraries and configurations accordingly[3][6].
- **DNS Resolution Defaults**: DNS resolution now defaults to IPv6 instead of IPv4. Applications relying on IPv4-specific behavior may need adjustments[9].

### **Node.js 18**
Node.js 18 builds on these changes and introduces additional breaking changes and deprecations.

#### **2.1. Removed or Deprecated APIs**
- **`dns.lookup()` with falsy hostname**: Passing a falsy hostname (e.g., `false`) to `dns.lookup()` is no longer supported. This behavior was undocumented and rarely used[4].
  - **Migration**: Ensure valid hostnames are passed to `dns.lookup()`.

- **`process.binding('uv').errname()`**: This private API is deprecated. Use `util.getSystemErrorName()` instead[4].
  - **Migration**: Replace calls to `process.binding('uv').errname()` with `util.getSystemErrorName()`.

- **Windows Performance Counter Support**: Deprecated and removed due to limited use[4].
  - **Migration**: Remove any reliance on Windows-specific performance counters.

- **`net._setSimultaneousAccepts()`**: This undocumented function is removed. It was used for debugging and performance tuning on Windows[4].
  - **Migration**: Remove calls to this function.

- **Trailing Slashes in Import Specifiers**: Specifiers ending with `/` in `import` or `exports` mappings are deprecated[4].
  - **Migration**: Update import/export mappings to avoid trailing slashes.

- **HTTP `.aborted` Property and Events**: The `.aborted` property and `'abort'`/`'aborted'` events in HTTP modules are deprecated. Use the Stream API's `.destroyed` property and `'close'` event instead[4].
  - **Migration**: Replace `.aborted` checks with `.destroyed` and listen for `'close'` events.

- **Thenable Support in Streams**: Streams no longer support thenables in implementation methods. Use callbacks instead[4].
  - **Migration**: Avoid using async functions in stream implementations.

#### **2.2. HTTP and Networking Changes**
- **HTTP Timeouts**: Default `headerTimeout` is now 60 seconds (previously 40 seconds), and `requestTimeout` is 5 minutes (previously unlimited)[6].
  - **Migration**: Adjust timeout configurations if relying on previous defaults.

- **Updated URL Parser**: Node.js 18 replaces the URL parser with Ada, compliant with the WHATWG URL specification, offering improved performance[7].
  - **Migration**: Test URL parsing logic for compatibility with the new parser.

#### **2.3. Cryptography**
- **RSA-PSS Key Pair Options**: The `'hash'` and `'mgf1Hash'` options are replaced with `'hashAlgorithm'` and `'mgf1HashAlgorithm'`[4].
  - **Migration**: Update cryptographic code to use the new option names.

#### **2.4. npm Updates**
- **npm 9**: Node.js 18 includes npm 9, which introduces breaking changes such as stricter handling of `package.json` fields and removal of deprecated commands like `npm bin`[10].
  - **Migration**: Review npm scripts and configurations for compatibility with npm 9.

#### **2.5. Global APIs**
- **Fetch API**: Node.js 18 introduces native support for the Fetch API, eliminating the need for third-party libraries like `node-fetch`[3][6].
  - **Migration**: Replace `node-fetch` or similar libraries with the native Fetch API.

- **Web Streams API**: Now globally available, enabling programmatic access to streams of data[3][6].
  - **Migration**: Use the Web Streams API for stream-based operations.

#### **2.6. Toolchain and Compiler**
- **V8 Engine Update**: Upgraded to version 10.1, introducing new JavaScript features like `findLast()` and `findLastIndex()` for arrays[6].
  - **Migration**: Test code for compatibility with the updated V8 engine.

## 3. Migration Guide with Examples

### **3.1. `dns.lookup()` with Falsy Hostname**
**Before:**
```javascript
dns.lookup(false, (err, address) => {
  console.log(address);
});
```

**After:**
```javascript
dns.lookup('localhost', (err, address) => {
  console.log(address);
});
```

### **3.2. HTTP `.aborted` Property**
**Before:**
```javascript
req.on('aborted', () => {
  console.log('Request aborted');
});
```

**After:**
```javascript
req.on('close', () => {
  if (req.destroyed) {
    console.log('Request aborted');
  }
});
```

### **3.3. Fetch API**
**Before:**
```javascript
const fetch = require('node-fetch');
fetch('https://api.example.com').then(res => res.json());
```

**After:**
```javascript
fetch('https://api.example.com').then(res => res.json());
```

### **3.4. RSA-PSS Key Pair Options**
**Before:**
```javascript
crypto.generateKeyPair('rsa', {
  modulusLength: 2048,
  publicExponent: 0x10001,
  hash: 'sha256',
  mgf1Hash: 'sha256',
}, callback);
```

**After:**
```javascript
crypto.generateKeyPair('rsa', {
  modulusLength: 2048,
  publicExponent: 0x10001,
  hashAlgorithm: 'sha256',
  mgf1HashAlgorithm: 'sha256',
}, callback);
```

### **3.5. npm Configuration**
**Before:**
```bash
npm bin
```

**After:**
```bash
npx
```

## Conclusion
Upgrading from Node.js 16 to Node.js 18 requires careful attention to breaking changes, deprecated APIs, and new features. By following this guide, you can ensure a smooth migration while taking advantage of the latest improvements in Node.js 18.