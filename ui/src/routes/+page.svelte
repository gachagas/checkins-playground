<script lang="ts">
	import * as Select from '$lib/components/ui/select/index.js';

	let value = $state('hello');
</script>

<section>
	<Select.Root type="single" bind:value>
		<Select.Trigger class="w-[180px]">This is the content</Select.Trigger>
		<Select.Content>
			<Select.Item value="light">Light</Select.Item>
			<Select.Item value="dark">Dark</Select.Item>
			<Select.Item value="system">System</Select.Item>
		</Select.Content>
	</Select.Root>
	<div class="text-red-500">The selected value is: {value}</div>
</section>
