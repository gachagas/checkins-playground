import { renderSnippet } from '$lib/components/ui/data-table/index.js';
import { renderComponent } from '$lib/components/ui/data-table/index.js';
import type { ColumnDef } from '@tanstack/table-core';
import { createRawSnippet } from 'svelte';
import DataTableEmailButton from './data-table-email-button.svelte';

// This type is used to define the shape of our data.
// You can use a Zod schema here if you want.
export type Checkin = {
  user: string;
  timestamp: number;
  hours: 'pending' | 'processing' | 'success' | 'failed';
  project: string;
};

export const columns: ColumnDef<Checkin>[] = [
  {
    accessorKey: 'user',
    header: ({ column }) =>
      renderComponent(DataTableEmailButton, {
        onclick: () => column.toggleSorting(column.getIsSorted() === 'asc'),
        name: 'user'
      })
  },
  {
    accessorKey: 'timestamp',
    header: ({ column }) =>
      renderComponent(DataTableEmailButton, {
        onclick: () => column.toggleSorting(column.getIsSorted() === 'asc'),
        name: 'timestamp'
      }),
    cell: ({ row }) => {
      return new Date(row.original.timestamp).toLocaleString();
    }
  },
  {
    accessorKey: 'hours',
    header: ({ column }) =>
      renderComponent(DataTableEmailButton, {
        onclick: () => column.toggleSorting(column.getIsSorted() === 'asc'),
        name: 'hours'
      })
  },
  {
    accessorKey: 'project',
    header: ({ column }) =>
      renderComponent(DataTableEmailButton, {
        onclick: () => column.toggleSorting(column.getIsSorted() === 'asc'),
        name: 'project'
      })
  }
  // {
  //   accessorKey: 'amount',
  //   header: () => {
  //     const amountHeaderSnippet = createRawSnippet(() => ({
  //       render: () => `<div class="text-right">Amount</div>`
  //     }));
  //     return renderSnippet(amountHeaderSnippet, '');
  //   },
  //   cell: ({ row }) => {
  //     const formatter = new Intl.NumberFormat('en-US', {
  //       style: 'currency',
  //       currency: 'USD'
  //     });

  //     const amountCellSnippet = createRawSnippet<[string]>((getAmount) => {
  //       const amount = getAmount();
  //       return {
  //         render: () => `<div class="text-right font-medium">${amount}</div>`
  //       };
  //     });

  //     return renderSnippet(amountCellSnippet, formatter.format(parseFloat(row.getValue('amount'))));
  //   }
  // }
];
