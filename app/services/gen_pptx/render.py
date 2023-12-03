import os
import jinja2

from ..gsheets.models import SheetRowTenderContent

from settings.config import settings

from pptx import Presentation  


async def render_text(input_path, model, output_path, jinja2_env):
    ppt = Presentation(input_path)
    for slide in ppt.slides:
        for shape in slide.shapes:
            if shape.has_text_frame:
                await _render_text_frame(shape.text_frame, model, jinja2_env)
    ppt.save(output_path)


async def _render_text_frame(text_frame, model, jinja2_env):
    last_ok = True
    tmp_str = ""
    tmp_runs = []
    for paragraph in text_frame.paragraphs:
        for run in paragraph.runs:
            cur_text = run.text
            tmp_str += cur_text
            tmp_runs.append(run)
            try:
                rtemplate = jinja2_env.from_string(tmp_str)
                rendered_text = rtemplate.render(model)

                for run in tmp_runs:
                    run.text = rendered_text
                    rendered_text = "" # overwrites text

                tmp_str = ""
                tmp_runs = []
                last_ok = True
            except Exception as e:
                #could not finish, i.e. have to append!
                last_ok = False


async def replace_images_by_shape_text(images: dict, template_path: str, output_path: str):
    # TODO: 
    #       - Удалять плейсхолдер shape после вставки картинки
    #       - Сделать фиксированный словарь плейсхолдеров и итерироваться по нему
    #       - Удалять плейсхолдер, если для него нет картинки
    prs = Presentation(template_path)
    for image in images:
        image_file = images[image]
        search_str = image
        for slide in prs.slides:
            for shape in slide.shapes:
                if shape.has_text_frame:
                    if shape.text.find(search_str) != -1:
                        if image_file:
                            horiz_ = shape.left
                            vert_ = shape.top
                            height_ = shape.height
                            width_ = shape.width
                            slide.shapes.add_picture(image_file, horiz_, vert_, width_, height_)
                        sp = shape._sp
                        sp.getparent().remove(sp)
    prs.save(output_path)


async def render_pptx(tender: SheetRowTenderContent, pictures: dict):
    model = {
        "address": tender.address,
        "subway_stations": tender.subway_stations,
        "region_name": tender.region_name,
        "district_name": tender.district_name,
        "object_area": tender.object_area,
        "floor": tender.floor,
        "applications_enddate": tender.applications_enddate,
        "deposit": tender.deposit,
        "start_price": tender.start_price,
        "m1_start_price": tender.m1_start_price,
    }

    jinja2_env = jinja2.Environment()

    if not os.path.isdir(settings.PPTX_OUTPUT_DIRPATH):
        os.mkdir(settings.PPTX_OUTPUT_DIRPATH)
    output_path = f'{settings.PPTX_OUTPUT_DIRPATH}/{tender.id}.pptx'
    await render_text(settings.PPTX_TEMPLATE_PATH, model, output_path, jinja2_env)
    await replace_images_by_shape_text(images=pictures, template_path=output_path, output_path=output_path)
    return output_path
