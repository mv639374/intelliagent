/** @type {import('next').NextConfig} */
const nextConfig = {
  // During development, proxy API requests to the backend server
  // to avoid CORS issues.
  async rewrites() {
    return [
      {
        source: "/api/:path*",
        destination: "http://localhost:8000/api/:path*", // Proxy to Backend
      },
    ];
  },
};

export default nextConfig;
