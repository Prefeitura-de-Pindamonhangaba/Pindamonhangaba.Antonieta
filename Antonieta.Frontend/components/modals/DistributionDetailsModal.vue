<template>
  <n-modal :show="modelValue" @update:show="$emit('update:modelValue', $event)" preset="dialog" style="width: 700px">
    <template #header>
      <div class="modal-header">
        <h3>Detalhes da Distribuição</h3>
      </div>
    </template>
    
    <div class="modal-content">
      <!-- Informações da Distribuição -->
      <n-divider title-placement="left">
        <span style="font-weight: 600; color: #f77800;">Informações da Distribuição</span>
      </n-divider>

      <n-grid :cols="2" :x-gap="12">
        <n-grid-item>
          <div class="info-field">
            <div class="info-label">👤 Beneficiário</div>
            <div class="info-value">{{ distribution?.beneficiaryName || 'N/A' }}</div>
          </div>
        </n-grid-item>
        <n-grid-item>
          <div class="info-field">
            <div class="info-label">🥫 Tipo de Ração</div>
            <div class="info-value">{{ distribution?.rationTypeName || 'N/A' }}</div>
          </div>
        </n-grid-item>
      </n-grid>

      <n-grid :cols="2" :x-gap="12">
        <n-grid-item>
          <div class="info-field">
            <div class="info-label">⚖️ Quantidade</div>
            <div class="info-value">{{ distribution?.amount?.toFixed(2) || '0.00' }}kg</div>
          </div>
        </n-grid-item>
        <n-grid-item>
          <div class="info-field">
            <div class="info-label">📅 Data da Distribuição</div>
            <div class="info-value">{{ distribution ? formatDate(distribution.date) : 'N/A' }}</div>
          </div>
        </n-grid-item>
      </n-grid>

      <!-- Observações -->
      <n-divider title-placement="left">
        <span style="font-weight: 600; color: #f77800;">Observações</span>
      </n-divider>

      <div class="observations-section">
        <div v-if="distribution?.observations && distribution.observations.trim()" class="observations-field">
          <div class="observations-text">
            {{ distribution.observations }}
          </div>
        </div>
        
        <div v-else class="no-observations">
          <n-text depth="3" style="font-style: italic;">
            📝 Nenhuma observação foi registrada para esta distribuição.
          </n-text>
        </div>
      </div>
    </div>

    <template #action>
      <div class="modal-actions">
        <n-button @click="handleClose">
          Fechar
        </n-button>
      </div>
    </template>
  </n-modal>
</template>

<script setup lang="ts">
import { defineProps, defineEmits } from 'vue'
import { 
  NModal, NText, NDivider, NButton, NIcon, NGrid, NGridItem, useMessage 
} from 'naive-ui'
import { IconCopy } from '@tabler/icons-vue'
import type { Distribution } from '~/models/distributionModel'

const props = defineProps<{
  modelValue: boolean
  distribution?: Distribution | null
}>()

const emit = defineEmits<{
  'update:modelValue': [value: boolean]
}>()

const message = useMessage()

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleString('pt-BR', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const handleClose = () => {
  emit('update:modelValue', false)
}
</script>

<style scoped>
/* ✅ Header (seguindo padrão) */
.modal-header h3 {
  margin: 0;
  color: #263238;
  font-size: 1.25rem;
  font-weight: 600;
}

/* ✅ Content (seguindo padrão) */
.modal-content {
  padding: 1rem 0;
  max-height: 70vh;
  overflow-y: auto;
}

/* ✅ Actions (seguindo padrão) */
.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
}

/* ✅ Divisores (seguindo padrão) */
:deep(.n-divider .n-divider__title) {
  font-size: 0.95rem;
}

/* ✅ SIMPLIFICADO: Campos de informação */
.info-field {
  margin-bottom: 16px;
}

.info-label {
  font-size: 14px;
  font-weight: 600;
  color: #666;
  margin-bottom: 6px;
}

.info-value {
  font-size: 15px;
  color: #333;
  background-color: #f8f9fa;
  padding: 10px 12px;
  border-radius: 6px;
  border-left: 3px solid #f77800;
}

/* ✅ SIMPLIFICADO: Seção de observações */
.observations-section {
  margin: 16px 0;
}

.observations-field {
  background-color: #f8f9fa;
  border-radius: 6px;
  border-left: 3px solid #52c41a;
  overflow: hidden;
}

.observations-text {
  padding: 16px;
  font-size: 14px;
  line-height: 1.6;
  color: #333;
  white-space: pre-wrap;
  word-break: break-word;
  max-height: 150px;
  overflow-y: auto;
}

.observations-actions {
  padding: 12px 16px;
  background-color: #f0f1f2;
  border-top: 1px solid #e0e0e0;
  text-align: right;
}

.no-observations {
  background-color: #f8f9fa;
  padding: 20px;
  border-radius: 6px;
  border: 2px dashed #d0d0d0;
  text-align: center;
}

/* ✅ Responsivo */
@media (max-width: 768px) {
  .modal-content {
    max-height: 60vh;
  }
}
</style>