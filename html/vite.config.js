import { defineConfig } from 'vite'
import { createSvgIconsPlugin } from 'vite-plugin-svg-icons'
const path = require('path')
import svgLoader from 'vite-svg-loader'
import vue from '@vitejs/plugin-vue'

// https://vitejs.dev/config/
export default defineConfig({
	plugins: [
		vue(),
		svgLoader(),
		createSvgIconsPlugin({
			// 指定需要缓存的图标文件夹
			iconDirs: [path.resolve(process.cwd(), 'src/icons')],
			// 指定symbolId格式
			symbolId: 'icon-[dir]-[name]',

			/**
			 * 自定义插入位置
			 * @default: body-last
			 */
			inject: 'body-last',

			/**
			 * custom dom id
			 * @default: __svg__icons__dom__
			 */
			customDomId: '__svg__icons__dom__',
		})
	],
	resolve: {
		alias: {
			'@': '/src'
		}
	},
	server: {
		proxy: {
			'/api': {
				target: 'http://127.0.0.1:8000',

			}
		}
	},
	envPrefix: "ENV_"

})
