const withNextra = require('nextra')({
  basePath: "MAT-4376E-F24",
  output: "export",
  theme: 'nextra-theme-docs',
  themeConfig: './theme.config.tsx',
})

module.exports = withNextra()
