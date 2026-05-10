// @ts-check
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';

// https://astro.build/config
export default defineConfig({
	site: 'https://mtpontes.github.io/docker-clean-pro/',
	base: '/docker-clean-pro',
	devToolbar: {
		enabled: false,
	},
	integrations: [
		starlight({
			title: 'Docker Clean Pro',
			social: [
				{ icon: 'github', label: 'GitHub', href: 'https://github.com/mtpontes/docker-clean-pro' },
			],
			defaultLocale: 'root',
			locales: {
				root: { label: 'English', lang: 'en' },
				'pt-br': { label: 'Português', lang: 'pt-BR' },
			},
			sidebar: [
				{
					label: 'Guides',
					items: [
						{ label: 'Installation', slug: 'guides/installation' },
						{ label: 'Quickstart', slug: 'guides/quickstart' },
					],
				},
				{
					label: 'Reference',
					items: [
						{ label: 'CLI Commands', slug: 'reference/commands' },
						{ label: 'Reporting', slug: 'reference/reporting' },
					],
				},
			],
		}),
	],
});
