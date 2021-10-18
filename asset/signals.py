import os
import csv
from io import StringIO
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver


from .models import Asset, BulkAssetUpload

@receiver(post_save, sender=BulkAssetUpload)
def create_bulk_asset(sender, created, instance, *args, **kwargs):
  if created:
    opened = StringIO(instance.csv_file.read().decode())
    reading = csv.DictReader(opened, delimiter=',')
    assets = []
    for row in reading:
      if 'asset_description' in row and row['asset_description']:
        asset_des = row['asset_description']
        tag = row['tag_number'] if 'tag_number' in row and row['tag_number'] else ''
        voucher_number = row['voucher_number'] if 'voucher_number' in row and row['voucher_number'] else ''
        sn = row['serial_number'] if 'serial_number' in row and row['serial_number'] else ''
        
        lcn = row['location'] if 'location' in row and row['location'] else ''
        ctg = row['category'] if 'category' in row and row['category'] else ''
        dis = row['date_in_service'] if 'date_in_service' in row and row['date_in_service'] else ''
       
        check = Asset.objects.filter(tag_number=tag).exists()
        if not check:
          assets.append(
            Asset(
                asset_description=asset_des,
                tag_number=tag,
               
                voucher_number=voucher_number,
                serial_number=sn,
                location=lcn,
                category=ctg,
                date_in_service=dis,
                
            )
          )

    Asset.objects.bulk_create(assets)
    instance.csv_file.close()
    instance.delete()


def _delete_file(path):
   """ Deletes file from filesystem. """
   if os.path.isfile(path):
       os.remove(path)

@receiver(post_delete, sender=BulkAssetUpload)
def delete_csv_file(sender, instance, *args, **kwargs):
  if instance.csv_file:
    _delete_file(instance.csv_file.path)


@receiver(post_delete, sender=Asset)
def delete_passport_on_delete(sender, instance, *args, **kwargs):

  if instance.passport:

    _delete_file(instance.passport.path)
