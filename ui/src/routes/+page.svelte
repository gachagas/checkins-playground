<script lang="ts">
  import CalendarIcon from 'lucide-svelte/icons/calendar';
  import type { DateRange } from 'bits-ui';
  import {
    CalendarDate,
    DateFormatter,
    type DateValue,
    getLocalTimeZone
  } from '@internationalized/date';
  import { cn } from '$lib/utils.js';
  import { buttonVariants } from '$lib/components/ui/button/index.js';
  import { RangeCalendar } from '$lib/components/ui/range-calendar/index.js';
  import * as Popover from '$lib/components/ui/popover/index.js';
  import { Input } from '$lib/components/ui/input/index.js';
  // rangepicker
  const df = new DateFormatter('en-US', {
    dateStyle: 'medium'
  });

  let value: DateRange = $state({
    start: new CalendarDate(2022, 1, 20),
    end: new CalendarDate(2022, 1, 20).add({ days: 20 })
  });

  let startValue: DateValue | undefined = $state(undefined);
</script>

<div class="min-h-screen bg-background p-8">
  <div class="mx-auto max-w-2xl space-y-8">
    <h1 class="text-3xl font-bold text-foreground">
      okay NOW we are hot reloading Welcome to SvelteKit today we shall hot reload
    </h1>
  </div>

  <div class="space-y-4">
    <div>
      {#if value?.start && value?.end}
        You have selected {value.start.toDate(getLocalTimeZone())} - {value.end.toDate(
          getLocalTimeZone()
        )}
      {:else}
        No date range selected
      {/if}
    </div>

    <!-- Input -->
    <div class=" grid w-fit gap-2">
      <Input type="text" placeholder="Enter name here..." />
    </div>

    <!-- rangepicker -->
    <div class=" grid w-fit gap-2">
      <Popover.Root>
        <Popover.Trigger
          class={cn(buttonVariants({ variant: 'outline' }), !value && 'text-muted-foreground')}
        >
          <CalendarIcon class="mr-2 size-4" />
          {#if value && value.start}
            {#if value.end}
              {df.format(value.start.toDate(getLocalTimeZone()))} - {df.format(
                value.end.toDate(getLocalTimeZone())
              )}
            {:else}
              {df.format(value.start.toDate(getLocalTimeZone()))}
            {/if}
          {:else if startValue}
            {df.format(startValue.toDate(getLocalTimeZone()))}
          {:else}
            Pick a date
          {/if}
        </Popover.Trigger>
        <Popover.Content class="w-auto p-0" align="start">
          <RangeCalendar
            bind:value
            onStartValueChange={(v) => {
              startValue = v;
            }}
            numberOfMonths={2}
          />
        </Popover.Content>
      </Popover.Root>
    </div>

    <!-- datatable -->
    <div>datatable</div>
  </div>
</div>
