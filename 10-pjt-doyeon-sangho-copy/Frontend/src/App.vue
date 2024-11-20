<script setup>
import ExchangeCalculator from './components/ExchangeCalculator.vue'
import BankLocator from './components/BankLocator.vue';
</script>

<template>
  <div>
    <header>
      <nav>
        <router-link to="/">Home</router-link>
        <router-link to="/exchange-calculator">Exchange Calculator</router-link>
        <router-link to="/deposits-detail">Deposit Comparison</router-link>
        <router-link to="/bank-locator">Find Nearby Banks</router-link>
      </nav>
    </header>

    <main>
      <ExchangeCalculator />
      <PlaceofBank />
    </main>
  </div>
</template>

<style scoped>
nav {
  display: flex;
  gap: 1rem;
  margin-bottom: 1rem;
}
</style>