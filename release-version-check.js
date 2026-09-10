const fs = require('fs');
const path = require('path');

const root = __dirname;
const read = f => fs.readFileSync(path.join(root, f), 'utf8');
const fail = m => { throw new Error('RELEASE_VERSION_CHECK: ' + m); };
const ok = (c, m) => { if (!c) fail(m); console.log('OK - ' + m); };
const semver = v => {
  const m = String(v || '').trim().match(/^[vV]?(\d+)\.(\d+)\.(\d+)$/);
  return m ? [Number(m[1]), Number(m[2]), Number(m[3])] : null;
};
const cmp = (a, b) => {
  const x = semver(a), y = semver(b);
  if (!x || !y) return null;
  for (let i = 0; i < 3; i++) if (x[i] !== y[i]) return x[i] > y[i] ? 1 : -1;
  return 0;
};

const index = read('index.html');
const sw = read('sw.js');
const install = read('install.html');
const latest = JSON.parse(read('latest-release.json'));
const nativeHtml = read('native.html');

const build = (index.match(/const\s+BUILD\s*=\s*['"]([^'"]+)['"]/) || [])[1] || '';
const appVersion = (sw.match(/const\s+APP_VERSION\s*=\s*['"]([^'"]+)['"]/) || [])[1] || '';
const cacheVersion = (sw.match(/const\s+V\s*=\s*['"]([^'"]+)['"]/) || [])[1] || '';
const installVersion = (install.match(/verifiedVersion\s*:\s*['"]([^'"]+)['"]/) || [])[1] || '';
const installApk = (install.match(/apkUrl\s*:\s*['"]([^'"]+)['"]/) || [])[1] || '';
const installRelease = (install.match(/releaseUrl\s*:\s*['"]([^'"]+)['"]/) || [])[1] || '';

ok(!!semver(build), 'index BUILD is full Vx.y.z: ' + build);
ok(appVersion === build, 'sw APP_VERSION matches index BUILD: ' + build);
const cachePrefix = 'ohg-v' + build.replace(/^V/i, '').replace(/\./g, '');
ok(cacheVersion.startsWith(cachePrefix), 'sw cache prefix matches BUILD: ' + cachePrefix);
ok(index.includes("([vV]\\d+(?:\\.\\d+){1,2})"), 'checkUpdate parser accepts Vx.y and Vx.y.z');
ok(!index.includes("([vV]\\d+(?:\\.\\d+)?)"), 'legacy two-component-only APP_VERSION parser is absent');

ok(index.includes("const DATA_SCHEMA = 6;"), 'DATA_SCHEMA remains 6');
ok(index.includes("const KEY = 'ohg.v1';"), 'personal recovery key remains ohg.v1');
ok(index.includes("const SOCIAL_KEY = 'ohg.social.v1';"), 'social key remains ohg.social.v1');

ok(!!semver(latest.version), 'latest-release version is full Vx.y.z: ' + latest.version);
ok(Number.isInteger(Number(latest.versionCode)) && Number(latest.versionCode) > 0, 'latest-release versionCode is valid: ' + latest.versionCode);
const latestTagPrefix = String(latest.version).toLowerCase();
ok(String(latest.apk || '').includes('/releases/download/' + latestTagPrefix), 'latest-release APK tag matches version');
ok(String(latest.apk || '').includes('/oneul-' + latestTagPrefix + '.apk'), 'latest-release APK filename matches version');
ok(String(latest.release || '').includes('/releases/tag/' + latestTagPrefix), 'latest-release page matches version');

ok(!!semver(installVersion), 'install verifiedVersion is full Vx.y.z: ' + installVersion);
const installTagPrefix = installVersion.toLowerCase();
ok(installApk.includes('/releases/download/' + installTagPrefix), 'install APK tag matches verifiedVersion');
ok(installApk.includes('/oneul-' + installTagPrefix + '.apk'), 'install APK filename matches verifiedVersion');
ok(installRelease.includes('/releases/tag/' + installTagPrefix), 'install release page matches verifiedVersion');
ok(cmp(installVersion, latest.version) <= 0, 'install recommendation is not newer than latest-release');
ok(/\^\\d\+\\\.\\d\+\\\.\\d\+\$/.test(nativeHtml), 'native appv marker accepts full x.y.z');

const expected = String(process.env.EXPECTED_APP_VERSION || '').trim().toUpperCase();
if (expected) {
  ok(!!semver(expected), 'EXPECTED_APP_VERSION is full Vx.y.z: ' + expected);
  ok(build.toUpperCase() === expected, 'index BUILD matches release target ' + expected);
  ok(appVersion.toUpperCase() === expected, 'sw APP_VERSION matches release target ' + expected);
  ok(String(latest.version).toUpperCase() === expected, 'latest-release version matches release target ' + expected);
}

const gradlePath = process.env.ANDROID_GRADLE;
if (gradlePath) {
  const gradle = fs.readFileSync(gradlePath, 'utf8');
  const versionCode = Number((gradle.match(/versionCode\s+(\d+)/) || [])[1] || 0);
  const versionName = (gradle.match(/versionName\s+['"]([^'"]+)['"]/) || [])[1] || '';
  const want = expected || build.toUpperCase();
  ok('V' + versionName === want, 'Android versionName matches release target: ' + versionName);
  ok(versionCode === Number(latest.versionCode), 'Android versionCode matches latest-release: ' + versionCode);
}

console.log('RELEASE VERSION CONSISTENCY PASS');
