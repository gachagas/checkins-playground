<script lang="ts">
  import { getUsers } from '$lib/api';
  import * as Select from '$lib/components/ui/select/index.js';
  import { createQuery } from '@tanstack/svelte-query';

  type Payment = {
    id: string;
    amount: number;
    status: 'pending' | 'processing' | 'success' | 'failed';
    email: string;
  };

  const data: Payment[] = [
    {
      id: '728ed52f',
      amount: 100,
      status: 'pending',
      email: 'm@example.com'
    },
    {
      id: '489e1d42',
      amount: 125,
      status: 'processing',
      email: 'example@gmail.com'
    }
  ];

  let value = $state('hello');

  const query = createQuery({
    queryKey: ['users'],
    queryFn: () => getUsers()
  });
</script>

<section>
  {value}

  <Select.Root type="single" disabled={$query.isPending || $query.isError} bind:value>
    <Select.Trigger class="px-5 w-[180px] m-2">
      {#if $query.isPending}
        Loading users...
      {:else if $query.isError}
        Error loading users
      {:else if $query.data?.data}
        {$query.data?.data[0]}
      {:else}
        Select a value
      {/if}
    </Select.Trigger>
    <Select.Content>
      <Select.Item value="light">Light</Select.Item>
      <Select.Item value="dark">Dark</Select.Item>
      <Select.Item value="system">System</Select.Item>
    </Select.Content>
  </Select.Root>
  <div class="text-red-500">The selected value is: {value}</div>
</section>
<section>
  <div>
    <h1>Checkins</h1>
  </div>
</section>
