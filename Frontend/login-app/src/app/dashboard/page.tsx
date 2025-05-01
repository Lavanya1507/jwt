// src/app/dashboard/page.tsx

'use client';

import { useEffect, useState } from 'react';

interface Profile {
  username: string;
  email: string;
  // Add any other fields from your FastAPI /profile response
}

export default function DashboardPage() {
  const [profile, setProfile] = useState<Profile | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function fetchProfile() {
      try {
        const res = await fetch('http://localhost:8000/profile', {
          credentials: 'include', // sends cookies
        });

        if (!res.ok) {
          throw new Error('Failed to fetch profile');
        }

        const data = await res.json();
        setProfile(data);
      } catch (err: any) {
        setError(err.message || 'An error occurred');
      }
    }

    fetchProfile();
  }, []);

  if (error) return <p className="text-red-500">Error: {error}</p>;
  if (!profile) return <p>Loading profile...</p>;

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-4">Welcome to your Dashboard</h1>
      <div className="bg-gray-100 p-4 rounded shadow">
        <p><strong>Username:</strong> {profile.username}</p>
        <p><strong>Email:</strong> {profile.email}</p>
      </div>
    </div>
  );
}
