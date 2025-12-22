<template>
  <page-wrapper :loading="pageLoading">
    <n-space vertical size="large">
      <!-- Header -->
      <div class="page-header">
        <n-h1>Administração de Usuários</n-h1>
        <n-divider class="divider" />
      </div>

      <!-- Search and Action Buttons -->
      <n-space justify="space-between" align="center">
        <search-field
          v-model:value="searchQuery"
          placeholder="Buscar por nome ou e-mail..."
          @search="handleSearch"
        />

        <app-button 
          type="primary"
          @click="openCreateModal"
        >
          <template #icon>
            <n-icon><IconUserPlus /></n-icon>
          </template>
          Adicionar Novo Usuário
        </app-button>
      </n-space>

      <!-- Table -->
      <n-card class="page-card">
        <n-data-table
          :columns="columns"
          :data="filteredUsers"
          :pagination="pagination"
          :loading="loading"
        />
      </n-card>

      <!-- User Modal -->
      <UserModal
        v-model="showUserModal"
        :edit-mode="!!selectedUser"
        :user="selectedUser"
        @submit="handleUserSubmit"
      />

      <!-- Delete Modal -->
      <n-modal
        v-model:show="showDeleteModal"
        preset="dialog"
        title="Confirmar Exclusão"
        content="Tem certeza que deseja excluir este usuário? Esta ação não pode ser desfeita."
        positive-text="Sim, Excluir"
        negative-text="Cancelar"
        @positive-click="confirmDelete"
        @negative-click="showDeleteModal = false"
      />
    </n-space>
  </page-wrapper>
</template>

<script setup lang="ts">
import { h, ref, onMounted, computed } from 'vue'
import {
  NSpace,
  NCard,
  NDataTable,
  NModal,
  NIcon,
  NH1,
  NDivider,
  NTag,
  useMessage,
  type DataTableColumns
} from 'naive-ui'
import { IconUserPlus, IconEdit, IconTrash } from '@tabler/icons-vue'
import UserModal from '../components/modals/UserModal.vue'
import ActionButtons from '../components/ActionButtons.vue'
import SearchField from '../components/SearchField.vue'
import AppButton from '../components/AppButton.vue'
import PageWrapper from '../components/PageWrapper.vue'
import User from '../models/userModel'
import { userService } from '~/services/userService'

definePageMeta({
  middleware: ['auth', 'admin']
})

const message = useMessage()
const users = ref<User[]>([])
const loading = ref(false)
const showUserModal = ref(false)
const showDeleteModal = ref(false)
const selectedUser = ref<User | null>(null)
const userToDelete = ref<number | null>(null)
const pageLoading = ref(true)
const searchQuery = ref('')

const pagination = {
  pageSize: 10,
  showSizePicker: true,
  pageSizes: [10, 20, 50, 100],
  showQuickJumper: true
}

// Filtrar usuários com base na busca
const filteredUsers = computed(() => {
  if (!searchQuery.value) return users.value
  
  const query = searchQuery.value.toLowerCase()
  return users.value.filter(user => 
    user.full_name.toLowerCase().includes(query) ||
    user.email.toLowerCase().includes(query)
  )
})

const columns: DataTableColumns<User> = [
  {
    title: 'Usuário',
    key: 'full_name',
    sorter: (a, b) => a.full_name.localeCompare(b.full_name),
    render(row) {
      return h('div', {}, [
        h('div', { style: 'font-weight: 500' }, row.full_name),
        h('div', { style: 'font-size: 12px; color: #999' }, row.email)
      ])
    }
  },
  {
    title: 'E-mail',
    key: 'email',
    sorter: (a, b) => a.email.localeCompare(b.email),
    ellipsis: {
      tooltip: true
    }
  },
  {
    title: 'Nível de Acesso',
    key: 'role',
    width: 150,
    render(row) {
      return h(
        NTag,
        {
          type: row.role === 'administrador' ? 'warning' : 'default',
          size: 'small'
        },
        { default: () => row.getRoleLabel() }
      )
    },
    sorter: (a, b) => a.role.localeCompare(b.role)
  },
  {
    title: 'Data de Criação',
    key: 'created_at',
    render(row) {
      return row.getFormattedCreatedAt()
    },
    sorter: (a, b) => {
      const dateA = a.created_at ? new Date(a.created_at).getTime() : 0
      const dateB = b.created_at ? new Date(b.created_at).getTime() : 0
      return dateA - dateB
    }
  },
  {
    title: 'Ações',
    key: 'actions',
    width: 150,
    render(row) {
      return h(ActionButtons, {
        onEdit: () => openEditModal(row),
        onDelete: () => openDeleteModal(row.id)
      })
    }
  }
]

const loadUsers = async () => {
  loading.value = true
  try {
    users.value = await userService.getAll()
  } catch (error) {
    console.error('Error loading users:', error)
    message.error('Erro ao carregar usuários')
  } finally {
    loading.value = false
    pageLoading.value = false
  }
}

const openCreateModal = () => {
  selectedUser.value = null
  showUserModal.value = true
}

const openEditModal = (user: User) => {
  selectedUser.value = user
  showUserModal.value = true
}

const openDeleteModal = (userId: number) => {
  userToDelete.value = userId
  showDeleteModal.value = true
}

const handleUserSubmit = async (userData: any) => {
  loading.value = true
  try {
    if (selectedUser.value) {
      // Editar usuário existente
      await userService.update(selectedUser.value.id, userData)
      message.success('Usuário atualizado com sucesso!')
    } else {
      // Criar novo usuário
      await userService.create(userData)
      message.success('Usuário criado com sucesso!')
    }
    
    showUserModal.value = false
    await loadUsers()
  } catch (error: any) {
    console.error('Error submitting user:', error)
    message.error(error.message || 'Erro ao salvar usuário')
  } finally {
    loading.value = false
  }
}

const confirmDelete = async () => {
  if (!userToDelete.value) return
  
  loading.value = true
  try {
    await userService.delete(userToDelete.value)
    message.success('Usuário excluído com sucesso!')
    await loadUsers()
  } catch (error: any) {
    console.error('Error deleting user:', error)
    message.error(error.message || 'Erro ao excluir usuário')
  } finally {
    loading.value = false
    showDeleteModal.value = false
    userToDelete.value = null
  }
}

const handleSearch = () => {
  // A filtragem é feita automaticamente pelo computed filteredUsers
}

onMounted(() => {
  loadUsers()
})
</script>

<style scoped>
.page-header {
  display: flex;
  flex-direction: column;
}

.page-header h1 {
  margin: 0;
  color: #f77800;
}

.divider {
  margin: 12px 0 0 0;
}

.page-card {
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}
</style>
