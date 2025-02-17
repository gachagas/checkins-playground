<script lang="ts">
  import { Button } from '$lib/components/ui/button/index.js';
  import ArrowUpDown from 'lucide-svelte/icons/arrow-up-down';
  import type { ComponentProps } from 'svelte';

  let {
    variant = 'ghost',
    name = 'sample_name',
    ...restProps
  }: ComponentProps<typeof Button> = $props();
</script>

<Button {variant} {...restProps}>
  {name}
  <ArrowUpDown class="ml-2" />
</Button>
