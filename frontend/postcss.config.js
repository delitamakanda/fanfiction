/* eslint-env node */
module.exports = {
  plugins: [
    require('postcss-flexbugs-fixes'),
    require('stylelint')({
      configFile: 'stylelint.config.js',
    }),
    require('postcss-import'),
    require('postcss-extend'),
    require('postcss-mixins'),
    // Comment out postcss-nested if you're using tailwindcss/nesting
    require('postcss-nested'),
    require('tailwindcss/nesting'),
    require('tailwindcss')('tailwind.config.js'),
    require('postcss-preset-env', {
      autoprefixer: {
        flexbox: 'no-2009',
      },
      stage: 3,
      features: {
        'custom-properties': false,
        'nesting-rules': false,
      },
    }),
    require('autoprefixer')(),
    require('postcss-reporter'),
    require('postcss-pseudo-classes'),
    require('@csstools/postcss-is-pseudo-class'),
    require('postcss-pseudo-is'),
  ],
};
