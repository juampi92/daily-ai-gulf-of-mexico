This is a [Next.js](https://nextjs.org) project bootstrapped with [`create-next-app`](https://nextjs.org/docs/app/api-reference/cli/create-next-app).

## Getting Started

First, run the development server:

```bash
npm run dev
# or
yarn dev
# or
pnpm dev
# or
bun dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

You can start editing the page by modifying `app/page.tsx`. The page auto-updates as you edit the file.

This project uses [`next/font`](https://nextjs.org/docs/app/building-your-application/optimizing/fonts) to automatically optimize and load [Geist](https://vercel.com/font), a new font family for Vercel.

## Learn More

To learn more about Next.js, take a look at the following resources:

- [Next.js Documentation](https://nextjs.org/docs) - learn about Next.js features and API.
- [Learn Next.js](https://nextjs.org/learn) - an interactive Next.js tutorial.

You can check out [the Next.js GitHub repository](https://github.com/vercel/next.js) - your feedback and contributions are welcome!

## Deploy on Vercel

The easiest way to deploy your Next.js app is to use the [Vercel Platform](https://vercel.com/new?utm_medium=default-template&filter=next.js&utm_source=create-next-app&utm_campaign=create-next-app-readme) from the creators of Next.js.

Check out our [Next.js deployment documentation](https://nextjs.org/docs/app/building-your-application/deploying) for more details.

## Deploy on GitHub Pages

This project is configured to be deployed to GitHub Pages using GitHub Actions. The workflow will:

1. Build the Next.js application with the correct base path (`/daily-ai-gulf-of-mexico`)
2. Deploy the static output to GitHub Pages

The base path is dynamically configured in `next.config.mjs` based on the environment:
- In development (local): No base path is used
- In GitHub Actions: Base path is set to `/daily-ai-gulf-of-mexico`

When you push changes to the `main` branch, the GitHub Action will automatically build and deploy your site.

To enable GitHub Pages:

1. Go to your repository settings
2. Navigate to "Pages" section
3. Select "GitHub Actions" as the source
4. The site will be available at `https://<username>.github.io/daily-ai-gulf-of-mexico/`

Note that the site uses a base path of `/daily-ai-gulf-of-mexico` in production, which is different from the development environment.
