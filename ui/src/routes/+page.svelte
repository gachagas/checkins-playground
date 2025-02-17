<script lang="ts">
  import { getUsers, getUserCheckins } from '$lib/api';
  import * as Select from '$lib/components/ui/select/index.js';
  import { createQuery } from '@tanstack/svelte-query';
  import DataTable from './payments/DataTable.svelte';
  import { columns } from './payments/columns';

  let selectedUser = $state('');

  let isUserCheckinsEnabled = $derived(selectedUser !== '');

  const users = createQuery({
    queryKey: ['users'],
    queryFn: () => getUsers()
  });

  const userCheckins = createQuery({
    queryKey: ['user-checkins'],
    queryFn: () => getUserCheckins(selectedUser),
    enabled: () => isUserCheckinsEnabled
  });

  $effect(() => {
    if ($users.data?.data && selectedUser === '') {
      selectedUser = $users.data?.data[0];
      $userCheckins.refetch();
    }
  });

  const triggerContent = $derived(selectedUser === '' ? 'Select a user...' : selectedUser);
</script>

<section>
  {#if $users.data?.data}say something{/if}
  {selectedUser !== ''}
  <Select.Root
    type="single"
    onValueChange={() => {
      $userCheckins.refetch();
    }}
    disabled={$users.isPending || $users.isError}
    bind:value={selectedUser}
  >
    <Select.Trigger class="px-5 w-[180px] m-2">
      {#if $users.isPending}
        Loading users...
      {:else if $users.isError}
        Error loading users
      {:else if $users.data?.data}
        {triggerContent}
      {:else}
        Unhandled State
      {/if}
    </Select.Trigger>
    <Select.Content>
      {#each $users.data?.data as user}
        <Select.Item value={user}>{user}</Select.Item>
      {/each}
    </Select.Content>
  </Select.Root>
</section>
{$userCheckins.data?.data.items[0].timestamp}
<section>
  {#if $userCheckins.isPending}
    Loading users...
  {:else if $userCheckins.isError}
    Error loading users
  {:else if $userCheckins.data?.data.items}
    <DataTable data={$userCheckins.data.data.items} {columns} />
  {:else}
    Select a value
  {/if}
</section>
