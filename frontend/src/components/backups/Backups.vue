<template>
  <div class="backups-container">
    <div class="card">
      <h2><i class="fas fa-database"></i> Gestión de Backups</h2>
      
      <div class="create-backup">
        <h3><i class="fas fa-plus-circle"></i> Crear Nuevo Backup</h3>
        <form @submit.prevent="createBackup" class="backup-form">
          <div class="form-row">
            <div class="form-group">
              <label for="backup-type">Tipo de Backup:</label>
              <select id="backup-type" v-model="backupType" required>
                <option value="">-- Seleccionar tipo --</option>
                <option value="completo">Completo</option>
                <option value="diferencial">Diferencial</option>
                <option value="incremental">Incremental</option>
              </select>
            </div>
            
            <div class="form-group">
              <label for="backup-file">Archivo de Backup:</label>
              <input type="file" id="backup-file" ref="fileInput" @change="handleFileChange" required>
            </div>
          </div>
          
          <div class="form-group">
            <label for="backup-description">Descripción:</label>
            <textarea id="backup-description" v-model="description" rows="3" 
              placeholder="Ingrese una descripción para este backup"></textarea>
          </div>
          
          <div class="form-actions">
            <button type="submit" class="btn-create">
              <i class="fas fa-plus"></i> Crear Backup
            </button>
          </div>
        </form>
      </div>
      
      <BackupList 
        :backups="backups" 
        :users="users"
        @download="handleDownload"
        @restore="handleRestore"
        @delete="handleDelete"
      />
    </div>
    
    <Modal 
      v-if="showModal"
      :title="modalTitle"
      :message="modalMessage"
      :confirmText="confirmText"
      @confirm="confirmAction"
      @cancel="showModal = false"
    />
  </div>
</template>

<script>
import { ref } from 'vue'
import BackupList from '@/components/backups/BackupList.vue'
import Modal from '@/components/common/ModalConfirm.vue'

export default {
  components: {
    BackupList,
    Modal
  },
  setup() {
    
    // Form data
    const backupType = ref('')
    const backupFile = ref(null)
    const description = ref('')
    const fileInput = ref(null)
    
    // Mock data
    const users = ref([
      { id: 1, username: 'admin' },
      { id: 2, username: 'user1' }
    ])
    
    const backups = ref([
      {
        id: 1,
        fecha_creacion: new Date(),
        tipo: 'completo',
        descripcion: 'Backup completo del sistema',
        tamaño: 1024 * 1024 * 5, // 5MB
        ubicacion: '/backups/system_full_2023',
        creado_por: { id: 1, username: 'admin' }
      },
      {
        id: 2,
        fecha_creacion: new Date(Date.now() - 86400000),
        tipo: 'incremental',
        descripcion: 'Backup incremental de la base de datos',
        tamaño: 1024 * 1024 * 2, // 2MB
        ubicacion: '/backups/db_incr_2023',
        creado_por: { id: 2, username: 'user1' }
      }
    ])
    
    // Modal
    const showModal = ref(false)
    const modalTitle = ref('')
    const modalMessage = ref('')
    const confirmText = ref('')
    let currentAction = null
    let currentBackupId = null
    
    function handleFileChange(event) {
      backupFile.value = event.target.files[0]
    }
    
    function createBackup() {
      if (!backupType.value) {
        toast.error('Seleccione un tipo de backup')
        return
      }
      
      // Simulate API call
      setTimeout(() => {
        const newBackup = {
          id: backups.value.length + 1,
          fecha_creacion: new Date(),
          tipo: backupType.value,
          descripcion: description.value || 'Sin descripción',
          tamaño: backupFile.value ? backupFile.value.size : 0,
          ubicacion: '/backups/new_backup_' + Date.now(),
          creado_por: { id: 1, username: 'admin' } // Mock current user
        }
        
        backups.value.unshift(newBackup)
        
        
        // Reset form
        backupType.value = ''
        description.value = ''
        if (fileInput.value) {
          fileInput.value.value = ''
        }
        backupFile.value = null
      }, 500)
    }
    
    function handleDownload(id) {
      toast.info(`Iniciando descarga del backup ${id}`)
    }
    
    function handleRestore(id) {
      currentBackupId = id
      modalTitle.value = 'Confirmar Restauración'
      modalMessage.value = `¿Está seguro que desea restaurar el backup #${id}?`
      confirmText.value = 'Restaurar'
      currentAction = 'restore'
      showModal.value = true
    }
    
    function handleDelete(id) {
      currentBackupId = id
      modalTitle.value = 'Confirmar Eliminación'
      modalMessage.value = `¿Está seguro que desea eliminar el backup #${id}? Esta acción no se puede deshacer.`
      confirmText.value = 'Eliminar'
      currentAction = 'delete'
      showModal.value = true
    }
    
    function confirmAction() {
      showModal.value = false
      
      if (currentAction === 'restore') {
        toast.info(`Restaurando backup ${currentBackupId}...`)
      } else if (currentAction === 'delete') {
        backups.value = backups.value.filter(b => b.id !== currentBackupId)
        toast.success(`Backup ${currentBackupId} eliminado`)
      }
      
      currentAction = null
      currentBackupId = null
    }
    
    return {
      backupType,
      description,
      fileInput,
      handleFileChange,
      users,
      backups,
      createBackup,
      handleDownload,
      handleRestore,
      handleDelete,
      showModal,
      modalTitle,
      modalMessage,
      confirmText,
      confirmAction
    }
  }
}
</script>

<style scoped>
.backups-container {
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
}

.card {
  background: white;
  border-radius: 10px;
  padding: 25px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.05);
}

.card h2 {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 20px;
  padding-bottom: 15px;
  border-bottom: 1px solid #eee;
  color: #2E7D32;
}

.create-backup {
  padding: 20px;
  background: #f9f9f9;
  border-radius: 8px;
  margin-bottom: 30px;
}

.create-backup h3 {
  margin-bottom: 15px;
  display: flex;
  align-items: center;
  gap: 8px;
  color: #2E7D32;
  font-size: 16px;
}

.backup-form {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.form-row {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 15px;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.form-group label {
  margin-bottom: 8px;
  font-weight: 500;
  color: #444;
  font-size: 14px;
}

.form-group select, 
.form-group input,
.form-group textarea {
  padding: 10px 12px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 14px;
  transition: border 0.3s;
}

.form-group select:focus, 
.form-group input:focus,
.form-group textarea:focus {
  border-color: #2E7D32;
  outline: none;
  box-shadow: 0 0 0 2px rgba(46, 125, 50, 0.2);
}

.form-group textarea {
  resize: vertical;
  min-height: 80px;
}

#backup-file {
  padding: 8px;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  margin-top: 10px;
}

.btn-create {
  background: linear-gradient(135deg, #2E7D32, #1B5E20);
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 6px;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: all 0.3s;
  font-size: 14px;
}

.btn-create:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(46, 125, 50, 0.3);
}
</style>