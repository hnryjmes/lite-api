# Generated by Django 3.2.11 on 2023-05-22 15:57

from django.db import migrations



def populate_inform_letter_template(apps, schema_editor):

    CASETYPE_SIEL_ID = "00000000-0000-0000-0000-000000000004"
    LICENSING_UNIT_ID = "58e77e47-42c8-499f-a58d-94f94541f8c6"
    ADVICETYPE_REFUSE_ID = "00000000-0000-0000-0000-000000000003"

    LetterLayout = apps.get_model("letter_layouts", "LetterLayout")
    LetterTemplates = apps.get_model("letter_templates", "LetterTemplate")
    PicklistItem = apps.get_model("picklists", "PicklistItem")
    Team = apps.get_model("teams", "Team")
       
    
    INFORM_LETTERS = [
        ("Weapons of mass destruction (WMD)", "wmd.txt"),
        ("Military and military", "mam.txt"),
        ("Military and weapons of mass destruction (WMD)", "mwmd.txt"),
    ]
    
     
    picklist_item_ids = []
        
    lu_team = Team.objects.get(pk=LICENSING_UNIT_ID)

    for inform_letter in INFORM_LETTERS:
        name, file_name = inform_letter
        with  open(f"lite_content/lite_api/letter_paragraphs/inform_letter_{file_name}", "r") as f:
            text = f.read()
            pick_list_item = PicklistItem.objects.create(
            team=lu_team,
            name=name,
            text=text,
            type="letter_paragraph",
            status="active",
            )
            pick_list_item.save()
            picklist_item_ids.append(pick_list_item.id)
    
    
    # Create the template 
    
    inform_letter_layout= LetterLayout.objects.create(
        name='Inform Letter', 
        filename="inform_letter"
    )
    inform_letter_layout.save()
    
    inform_letter_template = LetterTemplates.objects.create(
        name="Inform letter",
        layout=inform_letter_layout,
        visible_to_exporter=True, 
        include_digital_signature=True
    )
 
    inform_letter_template.letter_paragraphs.set(picklist_item_ids)
    inform_letter_template.case_types.set([CASETYPE_SIEL_ID])
    inform_letter_template.decisions.set([ADVICETYPE_REFUSE_ID])
    inform_letter_template.save()        


class Migration(migrations.Migration):

    dependencies = [
        ("letter_templates", "0003_populate_seed_data"),
    ]

    operations = [
        migrations.RunPython(populate_inform_letter_template, migrations.RunPython.noop),
    ]
