<template>
  <n-config-provider>
    <n-message-provider>
      <n-loading-bar-provider>
        <n-dialog-provider>
          <n-notification-provider>
            <div class="min-h-screen bg-gray-100">
              <NuxtPage />
            </div>
          </n-notification-provider>
        </n-dialog-provider>
      </n-loading-bar-provider>
    </n-message-provider>
  </n-config-provider>
</template>

<style>
html, body {
  margin: 0;
  padding: 0;
  font-family: 'Montserrat', sans-serif;
}
</style>
