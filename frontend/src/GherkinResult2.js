import * as React from 'react';
import { TreeView, TreeItem } from '@mui/x-tree-view';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import ChevronRightIcon from '@mui/icons-material/ChevronRight';
import Checkbox from "@mui/material/Checkbox";
import Tooltip from '@mui/material/Tooltip';
import Paper from '@mui/material/Paper';
import Table from '@mui/material/Table';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableBody from '@mui/material/TableBody';
import TableRow from '@mui/material/TableRow';
import TablePagination from '@mui/material/TablePagination';
import { statusToColor, severityToLabel, statusToLabel, severityToColor } from './mappings';

import { useEffect, useState } from 'react';

export default function GherkinResult2({ summary, content, status, instances }) {
  const [data, setRows] = React.useState([])
  const [page, setPage] = useState(0);
  const [checked, setChecked] = React.useState(false);

  const handleChangePage = (_, newPage) => {
    setPage(newPage);
  };  

  const handleChange = (event) => {
    setChecked(event.target.checked);
  };

  useEffect(() => {
    let grouped = [];
    let filteredContent = content.filter(function(el) {
      return checked || el.severity > 2;
    });
    filteredContent.sort((f1, f2) => f1.feature > f2.feature ? 1 : -1);

    for (let c of (filteredContent || [])) {
      if (grouped.length === 0 || (c.feature ? c.feature : 'Uncategorized') !== grouped[grouped.length-1][0]) {
        grouped.push([c.feature ? c.feature : 'Uncategorized',[]])
      }
      grouped[grouped.length-1][1].push(c);
    }

    // aggregate severity
    for (let g of (grouped || [])) {
      g[2] = Math.max(...g[1].map(f => f.severity))
    }

    // order features
    grouped.sort((f1, f2) => f1[0] > f2[0] ? 1 : -1);

    setRows(grouped)
  }, [page, content, checked]);

  return (
    <div>
      <TableContainer sx={{ maxWidth: 850 }} component={Paper}>
        <Table>
          <TableHead>
            <TableCell sx={{ borderColor: 'black', fontWeight: 'bold' }}>
              {summary}
            </TableCell>
            <TableCell sx={{ borderColor: 'black', fontSize: 'small', textAlign: 'right' }} >
              <Checkbox size='small'
                checked={checked}
                onChange={handleChange}
                tabIndex={-1}
                disableRipple
                color="default"
                label="test"
                />include Passed, Disabled and N/A &nbsp;
                <Tooltip title='This also shows Passed, Disabled and N/A rule results.'>
                  <span style={{ display: 'inline-block'}}>
                    <span style={{fontSize: '.83em', verticalAlign: 'super'}}>ⓘ</span>
                  </span>
                </Tooltip>
              </TableCell>
          </TableHead>
        </Table>
      </TableContainer>
       
    <Paper sx={{overflow: 'hidden',
          "width": "850px",
          ".MuiTreeItem-root .MuiTreeItem-root": { backgroundColor: "#ffffff80", overflow: "hidden" },
          ".MuiTreeItem-group .MuiTreeItem-content": { boxSizing: "border-box" },
          ".MuiTreeItem-group": { padding: "16px", marginLeft: 0 },
          "> li > .MuiTreeItem-content": { padding: "16px" },
          ".MuiTreeItem-content.Mui-expanded": { borderBottom: 'solid 1px black' },
          ".MuiTreeItem-group .MuiTreeItem-content.Mui-expanded": { borderBottom: 0 },
          ".caption" : { paddingTop: "1em", paddingBottom: "1em", textTransform: 'capitalize' },
          ".subcaption" : { visibility: "hidden", fontSize: '80%' },
          ".MuiTreeItem-content.Mui-expanded .subcaption" : { visibility: "visible" },
          "table": { borderCollapse: 'collapse', fontSize: '80%' },
          "td, th": { padding: '0.2em 0.5em', verticalAlign: 'top' },
          ".pre": {
            whiteSpace: 'pre-wrap',
            wordBreak: 'break-word',
            // overflowWrap: 'break-word'
          }
        }}
      >
        <div>
          { data.length
            ? data.map(([feature, rows, severity]) => {
                return <TreeView 
                  defaultCollapseIcon={<ExpandMoreIcon />}
                  defaultExpandIcon={<ChevronRightIcon />}                 
                  >
                    <TreeItem 
                      nodeId={feature} 
                      label={<div class='caption'>{feature}</div>} 
                      sx={{ "backgroundColor": severityToColor[severity] }}
                    >
                      <div>
                        ⓘ {rows[0].feature_text !== null ? rows[0].feature_text : '-'}
                        <br />
                        <br />
                        <a size='small' target='blank' href={rows[0].feature_url}>{rows[0].feature_url}</a>
                        <br />
                        <br />                        
                      </div>
                      <table width='100%' style={{ 'text-align': 'left'}}>
                        <thead>
                          <tr><th>Id</th><th>Entity</th><th>Severity</th><th>Expected</th><th>Observed</th><th>Message</th></tr>
                        </thead>
                        <tbody>
                          {
                            rows.map((row) => {
                              return <tr> 
                                <td>{row.instance_id ? (instances[row.instance_id] ? instances[row.instance_id].guid : '?') : '-'}</td>
                                <td>{row.instance_id ? (instances[row.instance_id] ? instances[row.instance_id].type : '?') : '-'}</td>
                                <td>{severityToLabel[row.severity]}</td>
                                <td>{row.expected ? row.expected : '-'}</td>
                                <td>{row.observed ? row.observed : '-'}</td>
                                <td>{row.message && row.message.length > 0 ? row.message : '-'}</td>                                
                            </tr>
                            })
                          }
                        </tbody>
                      </table>
                    </TreeItem>
                  </TreeView>
              })
            : <div style={{ margin: '0.5em 1em' }}>{statusToLabel[status]}</div> }
          {
            content.length
            ? <TablePagination
                sx={{display: 'flex', justifyContent: 'center'}}
                rowsPerPageOptions={[10]}
                component="div"
                count={content.length}
                rowsPerPage={50}
                page={page}
                onPageChange={handleChangePage}
              />
            : null
          }
        </div>
    </Paper>
    </div>
  );
}