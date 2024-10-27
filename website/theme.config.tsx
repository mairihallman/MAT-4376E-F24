import React from 'react'
import { DocsThemeConfig } from 'nextra-theme-docs'


const config: DocsThemeConfig = {
  logo: <span>MAT 4376 GROUP 1</span>,
  project: {
    link: 'https://github.com/mairihallman/MAT-4376E-F24',
  },
  docsRepositoryBase: 'https://github.com/mairihallman/MAT-4376E-F24',
  footer: {
    text: 'Team 1 Github',
  },
  darkMode: false,
  nextThemes: {
    defaultTheme: 'light',
    forcedTheme: 'light',
  }
}

export default config