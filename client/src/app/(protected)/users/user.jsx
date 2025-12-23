import Image from "next/image";
import { Button } from "@/components/ui/button";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { MoreHorizontal } from "lucide-react";
import { TableCell, TableRow } from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";
import { cn } from "@/lib/utils";
import { useState } from "react";

export function User({ user, setError, setShowAlert }) {
  const [isActive, setIsActive] = useState(user.is_active);

  const activateUser = async () => {
    try {
      const access_token = localStorage.getItem("access_token");
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_BACKEND_URL}/user/activate-user?user_id=${user.user_id}`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `${access_token}`,
          },
        }
      );

      if (!response.ok) {
        const errorData = await response.json();
        setError(errorData.message);
        setShowAlert(true);
        setTimeout(() => {
          setShowAlert(false);
        }, 3000);
        return;
      }
      setIsActive(1);
    } catch (error) {
      setError("Error activating account");
      setShowAlert(true);
      setTimeout(() => {
        setShowAlert(false);
      }, 3000);
    }
  };

  const deactivateUser = async () => {
    try {
      const access_token = localStorage.getItem("access_token");

      const response = await fetch(
        `${process.env.NEXT_PUBLIC_BACKEND_URL}/user/deactivate-user?user_id=${user.user_id}`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `${access_token}`,
          },
        }
      );

      if (!response.ok) {
        const errorData = await response.json();
        setError(errorData.message);
        setShowAlert(true);
        setTimeout(() => {
          setShowAlert(false);
        }, 3000);
        return;
      }

      setIsActive(0);
    } catch (error) {
      setError("Error deactivating account");
      setShowAlert(true);
      setTimeout(() => {
        setShowAlert(false);
      }, 3000);
    }
  };

  const deleteUser = async () => {
    try {
      const access_token = localStorage.getItem("access_token");

      const response = await fetch(
        `${process.env.NEXT_PUBLIC_BACKEND_URL}/user/delete-user?user_id=${user.user_id}`,
        {
          method: "DELETE",
          headers: {
            "Content-Type": "application/json",
            Authorization: `${access_token}`,
          },
        }
      );

      if (!response.ok) {
        const errorData = await response.json();
        setError(errorData.message);
        setShowAlert(true);
        setTimeout(() => {
          setShowAlert(false);
        }, 3000);
        return;
      }
      
      // Reload the page to reflect changes
      window.location.reload();
    } catch (error) {
      setError("Error deleting account");
      setShowAlert(true);
      setTimeout(() => {
        setShowAlert(false);
      }, 3000);
    }
  };

  function formatUserID(id) {
    return `U${id.toString().padStart(4, "0")}`;
  }

  return (
    <TableRow>
      <TableCell className="hidden w-[100px] sm:table-cell">
        <Image
          unoptimized
          src={user.image_url || "https://api.dicebear.com/9.x/pixel-art/svg"}
          alt="User Avatar"
          width={40}
          height={40}
          className="aspect-square rounded-md object-cover"
        />
      </TableCell>
      <TableCell className="font-medium">{formatUserID(user.user_id)}</TableCell>
      <TableCell className="font-medium">{user.username}</TableCell>
      <TableCell className="hidden md:table-cell">{user.email}</TableCell>
      <TableCell className="hidden md:table-cell">
        <Badge
          variant="outline"
          className={cn(
            "capitalize",
            user.role_name === "MANAGER"
              ? "border-gray-500 text-gray-500"
              : "border-blue-500 text-blue-500"
          )}
        >
          {user.role_name}
        </Badge>
      </TableCell>
      <TableCell>
        {isActive === 1 ? (
          <Badge variant="secondary" className="capitalize">
            Active
          </Badge>
        ) : (
          <Badge variant="destructive" className="capitalize">
            Inactive
          </Badge>
        )}
      </TableCell>
      <TableCell>
        <DropdownMenu>
          <DropdownMenuTrigger asChild>
            <Button aria-haspopup="true" size="icon" variant="ghost">
              <MoreHorizontal className="h-4 w-4" />
              <span className="sr-only">Toggle menu</span>
            </Button>
          </DropdownMenuTrigger>
          <DropdownMenuContent align="end">
            <DropdownMenuLabel>Actions</DropdownMenuLabel>
            <DropdownMenuItem>
              <button type="submit" onClick={activateUser}>
                Activate
              </button>
            </DropdownMenuItem>
            <DropdownMenuItem>
              <button type="submit" onClick={deactivateUser}>
                Deactivate
              </button>
            </DropdownMenuItem>
            <DropdownMenuItem>
              <button type="submit" onClick={deleteUser} className="text-red-600">
                Delete
              </button>
            </DropdownMenuItem>
          </DropdownMenuContent>
        </DropdownMenu>
      </TableCell>
    </TableRow>
  );
}
