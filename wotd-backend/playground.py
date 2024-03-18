from src.service.persistence_service import PersistenceService

print('before')
persistence = PersistenceService()
print('middle: ', persistence)
persistence.get_available_languages()
print('after: ', persistence)
