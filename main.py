from fastapi import FastAPI, Query, status as stat
from fastapi.encoders import jsonable_encoder
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel
from starlette.responses import Response

from calculation import solution
from comparison import compare, conversion

import uvicorn
import re

app = FastAPI()

# create our list of expressions
result = []


class Item(BaseModel):
    expression: str


@app.post('/calc')
async def calc(response: Response, item: Item):
    json_compatible_item_data = jsonable_encoder(item)
    expression = json_compatible_item_data['expression']
    mathematical_expression = conversion(expression)

    status = compare(mathematical_expression)
    if len(result) > 29:
        del result[0]
    if status == 'success':
        try:
            number = solution(mathematical_expression)
        except ZeroDivisionError:
            status = 'fail'
            answer = {expression: 'ZeroDivisionError'}
            result.append({'request': expression,
                           'response': '',
                           'status': status})
            response.status_code = stat.HTTP_400_BAD_REQUEST
            return answer

        if re.search(r'\.0$', str(number)):  # cut off leading zeros
            number = int(number)

        answer = {expression: str(round(number, 3))}
        result.append({'request': expression,
                       'response': str(round(number, 3)),
                       'status': status})

    elif status == 'fail':

        answer = {expression: 'wrong expression'}
        result.append({'request': expression,
                       'response': '',
                       'status': status})
        response.status_code = stat.HTTP_400_BAD_REQUEST

    return answer


@app.get('/history')
async def history(status: str = None, limit: int = Query(30, ge=1, le=30)):
    if limit in range(1, 31):

        if not status:
            lst = list(reversed(result))
            return lst[:limit]

        elif status in ['fail', 'success']:

            lst = list(reversed([expression for expression in result if expression['status'] == status]))
            return lst[:limit]

        # returns error if status wrong
        else:
            return PlainTextResponse('wrong status', status_code=400)


if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, host="127.0.0.1", reload=True)
