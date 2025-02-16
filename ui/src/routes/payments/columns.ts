import { renderSnippet } from '$lib/components/ui/data-table/index.js';
import type { ColumnDef } from '@tanstack/table-core';
import { createRawSnippet } from 'svelte';

// This type is used to define the shape of our data.
// You can use a Zod schema here if you want.
export type Payment = {
  id: string;
  amount: number;
  status: 'pending' | 'processing' | 'success' | 'failed';
  email: string;
};

export const columns: ColumnDef<Payment>[] = [
  {
    accessorKey: 'user',
    header: 'user'
  },
  {
    accessorKey: 'timestamp',
    header: 'TimeStamp'
  },
  {
    accessorKey: 'hours',
    header: 'Hours'
  },
  {
    accessorKey: 'project',
    header: 'Project'
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
