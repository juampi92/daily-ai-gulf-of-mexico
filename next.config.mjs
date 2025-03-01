/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'export', // Enables static HTML export
  distDir: 'out', // Output directory for the static build
  images: {
    unoptimized: true, // Required for static export
  },
  // Dynamically set basePath and assetPrefix based on environment
  basePath: process.env.GITHUB_ACTIONS ? '/daily-ai-gulf-of-mexico' : '',
  assetPrefix: process.env.GITHUB_ACTIONS ? '/daily-ai-gulf-of-mexico/' : '',
};

export default nextConfig;
