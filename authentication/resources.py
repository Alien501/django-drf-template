from import_export import resources
from .models import User

class UserResource(resources.ModelResource):
    class Meta:
        model = User
        skip_unchanged = True
        report_skipped = True
        import_id_fields = ['email']
        fields = ['first_name', 'last_name', 'email',]
        exclude = ['password']

    def before_import_row(self, row, **kwargs):
        """Set default password for new users only"""
        email = row.get('email')
        if not email:
            return
        
        # Store password in the row data to be used later
        if not User.objects.filter(email=email).exists():
            # For new users, set password
            row['password'] = "changeme@123"

    def import_row(self, row, instance_loader, **kwargs):
        """
        Override import_row to handle password setting
        """
        # Get or create instance
        instance, new = self.get_or_init_instance(instance_loader, row)
        
        # Process row normally
        row_result = super().import_row(row, instance_loader, **kwargs)
        
        if row_result.import_type != row_result.IMPORT_TYPE_SKIP:
            # If this is a new user and we have a password in the row
            if new and 'password' in row:
                # Get the saved instance from the result
                saved_instance = row_result.instance
                if saved_instance:
                    # Set password and save
                    saved_instance.set_password(row['password'])
                    saved_instance.save()
                    print(f"Password set for {saved_instance.email}")
        
        return row_result