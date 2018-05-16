module.exports = {
  staticFileGlobs: [
    'dist/**.css',
    'manifest.json',
    'dist/**.js',
    'dist/**.png',
    'dist/**.jpg',
  ],
  "stripPrefix": "/",
  "runtimeCaching": [{
    "handler": "networkFirst"
  }],
}
