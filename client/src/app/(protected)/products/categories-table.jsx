'use client';

import {
  TableHead,
  TableRow,
  TableHeader,
  TableBody,
  Table,
} from '@/components/ui/table';
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from '@/components/ui/card';
import { Category } from './category';
import { ChevronLeft, ChevronRight } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { useState } from 'react';

export function CategoriesTable({ categories, setError, setShowAlert, refreshCategories }) {
  const [offset, setOffset] = useState(0);
  const limit = 10;
  const totalCategories = categories.length;
  
  const paginatedCategories = categories.slice(offset, offset + limit);

  function prevPage(e) {
    e.preventDefault();
    if (offset - limit >= 0) {
      setOffset(offset - limit);
    }
  }

  function nextPage(e) {
    e.preventDefault();
    if (offset + limit < totalCategories) {
      setOffset(offset + limit);
    }
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>Categories</CardTitle>
        <CardDescription>Manage your product categories.</CardDescription>
      </CardHeader>
      <CardContent>
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>ID</TableHead>
              <TableHead>Name</TableHead>
              <TableHead>Description</TableHead>
              <TableHead>
                <span className="sr-only">Actions</span>
              </TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {paginatedCategories.map((category) => (
              <Category
                key={category.category_id}
                category={category}
                setError={setError}
                setShowAlert={setShowAlert}
                refreshCategories={refreshCategories}
              />
            ))}
            {categories.length === 0 && (
              <TableRow>
                <TableHead colSpan={4} className="text-center">
                  No categories found.
                </TableHead>
              </TableRow>
            )}
          </TableBody>
        </Table>
      </CardContent>
      <CardFooter>
        <form className="flex items-center w-full justify-between">
          <div className="text-xs text-muted-foreground">
            Showing{' '}
            <strong>
              {offset + 1}-{Math.min(offset + limit, totalCategories)}
            </strong>{' '}
            of <strong>{totalCategories}</strong> categories
          </div>
          <div className="flex">
            <Button
              onClick={prevPage}
              variant="ghost"
              size="sm"
              type="button"
              disabled={offset === 0}
            >
              <ChevronLeft className="mr-2 h-4 w-4" />
              Prev
            </Button>
            <Button
              onClick={nextPage}
              variant="ghost"
              size="sm"
              type="button"
              disabled={offset + limit >= totalCategories}
            >
              Next
              <ChevronRight className="ml-2 h-4 w-4" />
            </Button>
          </div>
        </form>
      </CardFooter>
    </Card>
  );
}
