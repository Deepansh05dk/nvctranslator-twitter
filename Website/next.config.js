/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  images: {
    remotePatterns: [
      {
        hostname: "pbs.twimg.com",
      },
    ],
  },
};

module.exports = nextConfig;