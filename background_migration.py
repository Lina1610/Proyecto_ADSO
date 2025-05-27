from flask_apscheduler import APScheduler
from datetime import datetime
import logging

class BackgroundMigrationService:
    def __init__(self, app):
        self.scheduler = APScheduler()
        self.scheduler.init_app(app)
        self.scheduler.start()
        
        # Configure logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def run_delivery_migrations(self):
        """
        Periodically run migrations for unassigned user IDs in deliveries
        """
        from migrations.migraciones import MigradorEntregas
        
        try:
            # Log start of migration
            self.logger.info(f"Starting background delivery migration at {datetime.now()}")
            
            # Call migration method
            migrated_count = MigradorEntregas.migrar_users_id()
            
            if migrated_count is not None:
                if migrated_count > 0:
                    self.logger.info(f"Successfully migrated {migrated_count} delivery records")
                else:
                    self.logger.info("No pending migrations found")
        except Exception as e:
            self.logger.error(f"Error in background delivery migration: {e}")

def setup_background_migrations(app):
    """Setup background migrations for the application"""
    migration_service = BackgroundMigrationService(app)
    
    # Schedule migration every 5 minutes
    migration_service.scheduler.add_job(
        id='delivery_migration_job', 
        func=migration_service.run_delivery_migrations, 
        trigger='interval', 
        minutes=5
    )
    return migration_service