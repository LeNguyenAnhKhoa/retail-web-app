"use client";

import { useEffect, useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import withAuth from "@/hooks/withAuth";

function ProfilePage() {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchUser = async () => {
      try {
        const token = localStorage.getItem("access_token");
        const response = await fetch(
          `${process.env.NEXT_PUBLIC_BACKEND_URL}/user/get-user-detail`,
          {
            headers: {
              Authorization: `${token}`,
            },
          }
        );
        if (response.ok) {
          const data = await response.json();
          setUser(data.data);
        }
      } catch (error) {
        console.error("Failed to fetch user details", error);
      } finally {
        setLoading(false);
      }
    };

    fetchUser();
  }, []);

  if (loading) {
    return <div>Your information is being loaded...</div>;
  }

  if (!user) {
    return <div>Failed to load user information.</div>;
  }

  return (
    <div className="flex justify-center p-8">
      <Card className="w-full max-w-md">
        <CardHeader>
          <CardTitle>Profile Information</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div>
            <label className="font-bold">Username:</label>
            <p>{user.username}</p>
          </div>
          <div>
            <label className="font-bold">Full Name:</label>
            <p>{user.full_name}</p>
          </div>
          <div>
            <label className="font-bold">Phone:</label>
            <p>{user.phone}</p>
          </div>
          <div>
            <label className="font-bold">Role:</label>
            <p>{user.role}</p>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}

export default withAuth(ProfilePage);
