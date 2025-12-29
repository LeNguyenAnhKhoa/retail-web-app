"use client";

import { useEffect, useState } from "react";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { UsersTable } from "./users-table";
import withAuth from "@/hooks/withAuth";
import { useSearchParams } from "next/navigation";

function UsersPage() {
  const [users, setUsers] = useState([]);
  const [error, setError] = useState(null);
  const [showAlert, setShowAlert] = useState(false);
  const searchParams = useSearchParams();
  const search = searchParams.get("search");

  useEffect(() => {
    const fetchUsers = async () => {
      try {
        const access_token = localStorage.getItem("access_token");
        let url = `${process.env.NEXT_PUBLIC_BACKEND_URL}/user/get-all-users`;
        if (search) {
          url += `?search=${search}`;
        }

        const response = await fetch(
          url,
          {
            method: "GET",
            headers: {
              "Content-Type": "application/json",
              Authorization: `${access_token}`,
            },
          }
        );

        if (!response.ok) {
          const errorData = await response.json();
          setError("Failed to fetch users");
          setShowAlert(true);
          setTimeout(() => {
            setShowAlert(false);
          }, 3000);
          return;
        }

        const data = await response.json();
        setUsers(data?.data || []);
      } catch (error) {
        setError("Error fetching users");
        setShowAlert(true);
        setTimeout(() => {
          setShowAlert(false);
        }, 3000);
      }
    };

    fetchUsers();
  }, [search]);

  return (
    <Tabs defaultValue="all">
      {showAlert && (
        <div
          className="fixed top-4 right-4 z-50 p-4 mb-4 text-sm text-red-800 rounded-lg bg-red-50 dark:bg-gray-800 dark:text-red-400 shadow-lg"
          role="alert"
        >
          {error}
        </div>
      )}
      <div className="flex items-center">
        <TabsList>
          <TabsTrigger value="all">All</TabsTrigger>
          <TabsTrigger value="active">Active</TabsTrigger>
          <TabsTrigger value="inactive">Inactive</TabsTrigger>
        </TabsList>
      </div>
      <TabsContent value="all">
        <UsersTable
          users={users}
          totalUsers={users.length}
          setError={setError}
          setShowAlert={setShowAlert}
        />
      </TabsContent>
      <TabsContent value="active">
        <UsersTable
          users={users.filter((user) => user.is_active)}
          totalUsers={users.filter((user) => user.is_active).length}
          setError={setError}
          setShowAlert={setShowAlert}
        />
      </TabsContent>
      <TabsContent value="inactive">
        <UsersTable
          users={users.filter((user) => !user.is_active)}
          totalUsers={users.filter((user) => !user.is_active).length}
          setError={setError}
          setShowAlert={setShowAlert}
        />
      </TabsContent>
    </Tabs>
  );
}

export default withAuth(UsersPage);
